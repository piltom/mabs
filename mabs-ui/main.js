// These two babies will be filled up by the on load by fetching from python
var array_types = undefined;

var wave_types = undefined;

var plot_types = undefined;

var myLayout = undefined;
var myArrayManager = undefined;
var mySignalManager = undefined;
var myPlotManager = undefined;
var mySignalList = undefined;

class BindManager {
  constructor(){
    this.elements = {};
  }

  registerElement(name, value, on_change_list){
    if(!this.elements.hasOwnProperty(name)){
      this.elements[name] = { 'value':value, 'onChangeList':on_change_list};
    }
  }

  setVal(name, val){
    return new Promise((rslv, rjct) => {
      if(!this.elements.hasOwnProperty(name)){
        rjct("Trying to access unregistered element: " + name);
      }else{
        this.elements[name].value = val;
        for(const onchangecb of this.elements[name].onChangeList)
          onchangecb();
        rslv(val);
      }
    });
  }
  emitOnChange(name){
    for(const onchangecb of this.elements[name].onChangeList)
      onchangecb();
  }
  pushToVal(name, val){
    return new Promise((rslv, rjct) => {
      if(!this.elements.hasOwnProperty(name)){
        rjct("Trying to access unregistered element: " + name);
      }else{
        this.elements[name].value.push(val);
        this.emitOnChange(name);
        rslv(val);
      }
    });
  }
  removeIdxFromVal(name, idx){
    if(!this.elements.hasOwnProperty(name)){
      return Promise.reject("Trying to access unregistered element: " + name);
    }else{
      if (this.elements[name].value.length > idx && idx>=0){
        this.elements[name].value.splice(idx,1)
        this.emitOnChange(name);
        Promise.resolve();
      }else{
        Promise.reject("Invalid index: " + idx);
      }
    }
  }
  removeWithFn(name, fn){
    if(!this.elements.hasOwnProperty(name)){
      return Promise.reject("Trying to access unregistered element: " + name);
    }else{
      let idx_del = this.elements[name].value.findIndex(fn);
      return this.removeIdxFromVal(name, idx_del);
    }
}
  getVal(name){
    if(!this.elements.hasOwnProperty(name)){
      throw "Trying to access unregistered element: " + name;
    }else{
      return JSON.parse(JSON.stringify(this.elements[name].value));
    }
  }
}

class genericElement {
  constructor(arrtype, config) {
    this.arrType = arrtype;
    this.parameters = JSON.parse(JSON.stringify(config[arrtype]));
  }

  setVal(key, val){
    this.parameters[key] = val;
  }

  getVal(key){
    return this.parameters[key].value;
  }

  getInfo(key){
    return this.parameters[key].description;
  }

  getType(key){
    return this.parameters[key].type;
  }
}

class genericElementEditor {
  constructor(container, identifier, config, buttons){
    this.types = Object.keys(config);
    this.element = new genericElement(this.types[0], config);
    this.config = config
    this.container = container;
    this.identifier = identifier;
    this.buttons = buttons;
    this.generateTable();
    this.newTypeSelected()
    $("#id"+identifier+"Type").change(() => this.newTypeSelected())
  }

  generateTable(){
    let myHtml = '<form id="idForm'+ this.identifier +'">';
    myHtml += '<label for="#id'+this.identifier+'Type"> '+this.identifier+' Type: </label><select name="'+this.identifier+'Type" id="id'+this.identifier+'Type">';
    for(const myType of this.types){
      myHtml += '<option value="' + myType + '"> ' + myType + '</option>';
    }
    myHtml += '</select><br><fieldset id="' + this.identifier + 'ParamSet">';
    myHtml += '</fieldset>'
    for(const button of this.buttons){
      myHtml += '<button type="button" id="idBtn'+ button.name + this.identifier + '">' + button.label + '</button></form>';
    }

    this.container.html(myHtml);
    for(const button of this.buttons)
      $('#idBtn' + button.name + this.identifier).click(button.onClick)
  }

  newTypeSelected(){
    this.element = new genericElement($("#id"+this.identifier+"Type")[0].value, this.config);
    let myHtml = "<legend>Parameters for " + this.element.arrType + "</legend>";
    for(const parameter of Object.keys(this.element.parameters)){
      myHtml += '<label title="' + this.element.getInfo(parameter) + '" for="id'+ this.identifier + parameter + '">'+ parameter+':</label>';
      myHtml += '<input type="' + this.element.getType(parameter) + '" id="id'+ this.identifier + parameter +'" name="name'+ parameter +'" value="'+ this.element.getVal(parameter) +'"><br>'
    };
    $("#" +this.identifier + "ParamSet").html(myHtml);
  }

  saveValuesToElement(){
    for(const parameter of Object.keys(this.element.parameters)){
      this.element.setVal(parameter, $('#id'+ this.identifier+ parameter)[0].value);
    }
  }
}

class valuesListBox{
  constructor(container, identifier, initialValues){
    this.container = container;
    this.values = initialValues;
    this.identifier = identifier;
    this.generateHtml();
    this.filloutOptions();
  }

  generateHtml(){
    let myHtml ='<select style="min-width: 300px;" name="' + this.identifier + '" id="idBox' + this.identifier + '" size="10"></select>';
    this.container.html(myHtml);
  }

  filloutOptions(){
    let myHtml = '';
    for(const val of this.values){
      myHtml += '<option value="'+ val.id +'">' + val.name + '</option>';
    }
    $('#idBox' + this.identifier).html(myHtml);
  }
  update(){
    this.values = GlobBinder.getVal("signal_list");
    this.filloutOptions()
  }

  getSelected(){
    return this.container.find(":selected").val();
  }
}

class UNameFactory{
  constructor(){
    this.taken = {};
  }
  get(basename){
    if(this.taken.hasOwnProperty(basename)){
      this.taken[basename] +=1;
    }else{
      this.taken[basename] = 0;
    }
    return basename + this.taken[basename];
  }
}
var config1 = {
  settings: {
    selectionEnabled: true
  },
  content: [{
        type: 'row',
        content: [
          {
            type: 'component',
            componentName: 'welcome',
            componentState: { label: 'Welcome' }
          }]
        }]
};

var GlobBinder = new BindManager();
var GlobUNameFactory = new UNameFactory();

function submit_array(){
  myArrayManager.saveValuesToElement();
  fetch("/micarray", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify($('#idForm' + myArrayManager.identifier).serializeArray())
  }).then(console.log(JSON.stringify($('#idForm' + myArrayManager.identifier).serializeArray())))
}

function add_signal(){
  mySignalManager.saveValuesToElement();
  let newid = GlobUNameFactory.get("signal");
  GlobBinder.pushToVal("signal_list", {"id": newid, "name": newid, "param":JSON.stringify(mySignalManager.element.parameters)});
}

function rmv_signal(){
  let idtoremove = mySignalList.getSelected();
  console.log(idtoremove);
  GlobBinder.removeWithFn("signal_list", (el) => el.id == idtoremove);
}

function upd_signal(){
  console.log("upd_signal")
}

function add_plot(){
  myPlotManager.saveValuesToElement();
  if( myLayout.selectedItem === null ) {
      alert( 'No item selected' );
  } else {
      myLayout.selectedItem.addChild({
        type:'component',
        componentName:'plotComponent',
        componentState:{"uid": GlobUNameFactory.get("plot"), "plotType":myPlotManager.element.arrType, "params":JSON.parse(JSON.stringify(myPlotManager.element.parameters))}
      });
  }
}

$( document ).ready( () =>{
  fetch("/interfaceobjects")
  .then(response => response.json())
  .then( iface_obj => {
    myLayout = new GoldenLayout( config1, $('#layoutContainer'));
    myLayout.registerComponent( 'welcome', function( container, componentState ){
        container.getElement().html( '<h2>' + componentState.label + '</h2>' );
    });
    myLayout.registerComponent( 'plotComponent', function( container, componentState){
      let container_elem = container.getElement();
      let req_url = '/plotimage?type=' + componentState.plotType;
      for(param of Object.keys(componentState.params))
          req_url += '&' + param + '=' + componentState.params[param];
      fetch(req_url)
      .then(resp => resp.text())
      .then( imgdata => {
        container_elem.css('background-color', 'white');
        container_elem.html('<img style="margin: auto; display:block;max-width:100%; max-height:100%;" id="id' + componentState.uid + '" src="data:image/png;base64, ' + imgdata +'"/>')
      })
    });
    array_types = iface_obj["array_types"];
    wave_types = iface_obj["wave_types"];
    plot_types = iface_obj["plot_types"];
    myLayout.init();

    let array_btns = [{"label":"Set", "name":"Set", "onClick":submit_array}]
    myArrayManager = new genericElementEditor($("#arraymenu"), "Array", array_types, array_btns);

    let signal_btns = [{"label":"Add new","name":"Add", "onClick":add_signal},
                       {"label":"Remove","name":"Rmv", "onClick":rmv_signal},
                       {"label":"Change Selected","name":"Chg", "onClick":upd_signal}]
    mySignalManager = new genericElementEditor($("#signalmenu"), "Signal", wave_types, signal_btns);

    let plot_btns = [{"label":"Plot","name":"plt", "onClick":add_plot}]
    myPlotManager = new genericElementEditor($("#plotmenu"), "Plots", plot_types, plot_btns);

    mySignalList = new valuesListBox($("#signallist"), "SignalList", []);

    GlobBinder.registerElement("signal_list", [], [()=>(mySignalList.update())]);

    $(window).resize(function () {
      myLayout.updateSize($(window).width()-330, $(window).height()-40);
    });
    myLayout.updateSize($(window).width()-330, $(window).height()-40);
  })
});
