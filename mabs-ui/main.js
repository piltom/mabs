// These two babies will be filled up by the on load by fetching from python
var array_types = undefined;

var wave_types = undefined;

var plot_types = undefined;

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

  pushToVal(name, val){
    return new Promise((rslv, rjct) => {
      if(!this.elements.hasOwnProperty(name)){
        rjct("Trying to access unregistered element: " + name);
      }else{
        this.elements[name].value.push(val);
        for(const onchangecb of this.elements[name].onChangeList)
          onchangecb();
        rslv(val);
      }
    });
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
  constructor(container, identifier, config, onAdd){
    this.types = Object.keys(config);
    this.element = new genericElement(this.types[0], config);
    this.config = config
    this.container = container;
    this.identifier = identifier;
    this.onAdd = onAdd;
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
    myHtml += '</fieldset><button type="button" id="idSubmit' + this.identifier + '">Set</button></form>';
    this.container.html(myHtml);
    $('#idSubmit' + this.identifier).click(() => { this.onAdd() })
  }

  newTypeSelected(){
    this.element = new genericElement($("#id"+this.identifier+"Type")[0].value, this.config);
    let myHtml = "<legend>Parameters for " + this.element.arrType + "</legend>";
    for(const parameter of Object.keys(this.element.parameters)){
      myHtml += '<label title="' + this.element.getInfo(parameter) + '" for="id' + parameter + '">'+ parameter+':</label>';
      myHtml += '<input type="' + this.element.getType(parameter) + '" id="id'+ parameter +'" name="name'+ parameter +'" value="'+ this.element.getVal(parameter) +'"><br>'
    };
    $("#" +this.identifier + "ParamSet").html(myHtml);
  }

  saveValuesToElement(){
    for(const parameter of Object.keys(this.element.parameters)){
      this.element.setVal(parameter, $('#id'+ parameter)[0].value);
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
    let myHtml ='<select name="' + this.identifier + '" id="idBox' + this.identifier + '" size="10"></select>';
    this.container.html(myHtml);
  }

  filloutOptions(){
    let myHtml = '';
    for(const val of this.values){
      myHtml += '<option value="'+ val.idx +'">' + val.name + '</option>';
    }
    $('#idBox' + this.identifier).html(myHtml);
  }
  update(){
    this.values = GlobBinder.getVal("signal_list");
    this.filloutOptions()
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


$( document ).ready( () =>{
  fetch("/interfaceobjects")
  .then(response => response.json())
  .then( iface_obj => {
    var myLayout = new GoldenLayout( config1, $('#layoutContainer'));
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
        container_elem.html('<img id="id' + componentState.uid + '" src="data:image/png;base64, ' + imgdata +'"/>')
      })
    });
    array_types = iface_obj["array_types"];
    wave_types = iface_obj["wave_types"];
    plot_types = iface_obj["plot_types"];
    myLayout.init();
    var myArrayManager = new genericElementEditor($("#arraymenu"), "Array", array_types, () => {
      myArrayManager.saveValuesToElement();
      fetch("/micarray", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify($('#idForm' + myArrayManager.identifier).serializeArray())
      }).then(console.log(JSON.stringify($('#idForm' + myArrayManager.identifier).serializeArray())))
    });

    var mySignalManager = new genericElementEditor($("#signalmenu"), "Signal", wave_types, () => {
      mySignalManager.saveValuesToElement();
      GlobBinder.pushToVal("signal_list", {"name": GlobUNameFactory.get("signal"),"param":JSON.stringify(mySignalManager.element.parameters)});
    });

    var myPlotManager = new genericElementEditor($("#plotmenu"), "Plots", plot_types, () => {
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

    });

    mySignalList = new valuesListBox($("#signallist"), "SignalList", []);

    GlobBinder.registerElement("signal_list", [], [()=>(mySignalList.update())]);

    $(window).resize(function () {
      myLayout.updateSize($(window).width()-330, $(window).height()-40);
    });
    myLayout.updateSize($(window).width()-330, $(window).height()-40);
  })
});
