import matplotlib
matplotlib.use('Agg')
import base64
from io import BytesIO
import json
import engine.plotter as eplt
import engine.directivity as dr
import engine.timesim as ts
import models.soundwave as ms
import models.micarrays as ma
import models.processors as mp
from flask import Flask, jsonify, request


app = Flask(__name__,
            static_url_path='',
            static_folder='mabs-ui',
            template_folder='mabs-ui')

array_types = {
  "ULA": {
    "K": {
      "description": "Number of microphones",
      "value": 7,
      "type": "number"
      },
    "L": {
      "description": "Length of array [meters]",
      "value": 1,
      "type": "number"
    }
  },
  "SemiCoprime": {
    "N": {
      "description": "Number of microphones for subarray 1",
      "value": 7,
      "type": "number"
      },
    "M": {
      "description": "Number of microphones for subarray 2",
      "value": 5,
      "type": "number"
      },
    "L": {
      "description": "Length of array [meters]",
      "value": 1,
      "type": "number"
    }
  }
}
wave_types = {
  "Sin": {
      "Amplitude": {
        "description": "Amplitude of wave",
        "value": 5,
        "type": "number"
        },
      "Phi": {
          "description": "Angle phi",
          "value": 7,
          "type": "number"
      },
      "Frequency": {
          "description": "Frequency",
          "value": 1,
          "type": "number"
          },
      "Phase": {
          "description": "Phase",
          "value": 30,
          "type": "number"
          },
      "Tstart": {
          "description": "Signal start in ms",
          "value": 0,
          "type": "number"
          },
      "Tend": {
           "description": "Signal end in ms",
           "value": 1000,
           "type": "number"
           }
  },
    "Square": {
        "Amplitude": {
          "description": "Amplitude of wave",
          "value": 5,
          "type": "number"
          },
        "Frequency": {
            "description": "Frequency",
            "value": 1000,
            "type": "number"
        }
    }
}

plot_types = {
    "directivity_colormap": {
        "MaxFrequency": {
          "description": "Maximum frequency of the plot",
          "value": 10000,
          "type": "number"
          },
        "MinFrequency": {
            "description": "Minimum frequency of the plot",
            "value": 50,
            "type": "number"
            },
        "StepFrequency": {
          "description": "Step used for simulation",
          "value": 50,
          "type": "number"
          }
        },
    "directivity_polar": {
        "Frequency": {
          "description": "Design frequency",
          "value": 1500,
          "type": "number"
          }
    },
    "timesim_time": {
        "Tstart": {
            "description": "Time start in ms",
            "value": 0,
            "type": "number"
        },
        "Tend": {
            "description": "Time end in ms",
            "value": 1000,
            "type": "number"
        }
    }
}


def getParam(name, param_list):
    return [theval["value"] for theval in param_list if theval["name"] == name][0]


def filloutParamsFromList(pattern, param_list):
    ret_dict = {}
    for mykey in pattern:
        ret_dict[mykey] = getParam("name" + mykey, param_list)
    return ret_dict


class SimulationManager():
    """docstring for SimulationManager."""

    def __init__(self):
        self.micArray = ma.ULAArray(5, 1)
        self.signals = []
        self.signal_list = []
        self.processor = mp.MinWindowProcessor(1)
        self.sim = ts.BaseTimeSim(self.micArray, self.signals, self.processor,
                                  [0, 40], 0.01, name="TestSim")

    def instantiateMicArray(self, params):
        arrType = getParam("ArrayType", params)
        micParam = filloutParamsFromList(array_types[arrType],
                                         [par for par in params if par["name"] != "ArrayType"])
        self.micArray = ma.unpackInstantiate(arrType, micParam)

    def processSignalList(self):
        self.signals = []
        for sig in self.signal_list:
            param = sig['param']
            if sig['type'] == "Sin":
                self.signals.append(
                    ms.sin([int(param['Phi']['value']), 0],
                            float(param['Amplitude']['value']),
                            int(param['Frequency']['value']),
                            [int(param['Tstart']['value']),int(param['Tend']['value'])])
                )
        for sig in self.signals:
            print(sig)

mySimManager = SimulationManager()


@ app.route('/micarray', methods=['POST'])
def set_mic_array():
    data = json.loads(request.data, strict=False)
    mySimManager.instantiateMicArray(data)
    return '', 204

@ app.route('/signal_list', methods=['POST'])
def set_signal_list():
    data = json.loads(request.data, strict=False)
    mySimManager.signal_list = data
    mySimManager.processSignalList()
    return '', 204


@ app.route('/currentsignallist', methods=['GET'])
def get_signal_list():
    return {'list': mySimManager.signal_list}


@ app.route('/interfaceobjects', methods=['GET'])
def get_iface_obj():
    return {"array_types": array_types, "wave_types": wave_types, "plot_types": plot_types}


@ app.route('/currentarray', methods=['GET'])
def get_curr_array():
    return {"type": "ULA", "params": array_types["ULA"]}


@ app.route('/plotimage', methods=['GET'])
def get_plotimage():
    plot_type = request.args.get("type")
    if plot_type == "directivity_colormap":
        f_range = [int(request.args.get("MinFrequency")),
                   int(request.args.get("MaxFrequency")),
                   int(request.args.get("StepFrequency"))]
        directivity, flabels = dr.prodprocdirectivity_fsweep(
                mySimManager.micArray.micPos, f_range, 0)
        image = BytesIO()
        eplt.plotColormap(directivity,
                          y_labels=flabels,
                          save_to=image,
                          text={"ylabel": "Frequency [Hz]",
                                "xlabel": "Angle [deg]",
                                "title": "Directivity " + str(mySimManager.micArray)})
        return base64.encodebytes(image.getvalue())
    elif plot_type == "directivity_polar":
        f_design = int(request.args.get("Frequency"))
        directivity = dr.prodprocdirectivity(
            mySimManager.micArray.micPos, f_design)
        image = BytesIO()
        eplt.plotPolar(
            list(range(360)),
                 directivity[0, :],
                 save_to=image,
                 text={"title": "Directivity " + str(mySimManager.micArray) + "\nFrequency: %d Hz" % f_design})
        return base64.encodebytes(image.getvalue())
    elif plot_type == "timesim_time":
        t_start = int(request.args.get("Tstart"))
        t_end = int(request.args.get("Tend"))

        timesim1 = ts.BaseTimeSim(mySimManager.micArray,
                                  mySimManager.signals,
                                  mySimManager.processor,
                                  [t_start,t_end],
                                  0.01,
                                  name="TestSim")
        image = BytesIO()
        eplt.plotSim(timesim1, save_to=image)
        return base64.encodebytes(image.getvalue())
    else:
        return ""
