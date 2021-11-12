from flask import Flask, jsonify, request
import models.processors as mp
import models.micarrays as ma
import models.soundwave as ms
import engine.timesim as ts
import engine.directivity as dr
import engine.plotter as eplt
import json
from io import BytesIO
import base64
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
      "Theta": {
          "description": "Angle Theta",
          "value": 1,
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
        self.processor = mp.MinWindowProcessor(1)
        self.sim = ts.BaseTimeSim(self.micArray, self.signals, self.processor,
                                  [0, 40], 0.01, name="TestSim")

    def instantiateMicArray(self, params):
        arrType = getParam("ArrayType", params)
        micParam = filloutParamsFromList(array_types[arrType],
                                         [par for par in params if par["name"] != "ArrayType"])
        self.micArray = ma.unpackInstantiate(arrType, micParam)
        print(self.micArray)


mySimManager = SimulationManager()


@ app.route('/micarray', methods=['POST'])
def set_mic_array():
    data = json.loads(request.data, strict=False)
    mySimManager.instantiateMicArray(data)
    return '', 204


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
        eplt.plotColormap(directivity, y_labels=flabels, save_to=image)
        return base64.encodebytes(image.getvalue())
    else:
        return ""
