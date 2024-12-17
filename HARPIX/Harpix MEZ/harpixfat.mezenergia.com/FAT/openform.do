<!DOCTYPE html>
<html class="w-100 overflow-sm-hidden">
<head>
<meta charset="ISO-8859-1">
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Abas - Formul&#225;rio de Login New</title>
<script type="text/javascript">
var orderTab = [1051797, 1051798, 1051799, 1051795, 1051796, 1051802, 1051800];
var detailPanelComponentsTab = new Map();
var pfstart = new Date().getTime();
</script>
<script type="text/javascript" src="assets/jquery.min.js"></script>
<script type="text/javascript" src="assets/bootstrap.min.js"></script>
<script type="text/javascript" src="assets/bootstrap-submenu.min.js"></script>
<script type="text/javascript">const showMessageAsLegacy = false</script>
<script type="text/javascript">const messageConfig = {};</script>
<script type="text/javascript" src="components/HTMLMessage.js?hash=30324577082526a1ba48b820bc39107e"></script>
<script type="text/javascript" src="components/sweetalert/sweetalert.min.js?hash=9227ef98d65cec0cd216630d8f786426"></script>
<script type="text/javascript" src="wfr.js?hash=3a9f496b0ced97f82a60784c65afc1da"></script>
<script type="text/javascript">var isomorphicDir = 'components/isomorphic/';
window.isc_loadCustomFonts = false;</script>
<script type="text/javascript" src="components/isomorphic/grid.min.js?hash=57d0aa71b73bb1e461a4131d41cd787c" defer></script>
<script type="text/javascript" src="components/isomorphic/skins/default/load_skin.js?hash=42c727301a9001d4983dcfba627f82f2" defer></script>
<link rel="stylesheet" type="text/css" href="components/isomorphic/skins/default/skin_styles.css?hash=465cfe106536e9eddd7d8f1129e70196"></link>
<script type="text/javascript" src="components/isomorphic/locales/frameworkMessages_pt.js?hash=bc177487f7c320c65199391b08aaf121" defer></script>
<script type="text/javascript" src="components/chart/echarts.min.js?hash=5d25be175d695d6bfc3441da7759d237" defer></script>
<script type="text/javascript" src="rulesFunctions.js?hash=6486699a8219fd518aa901b2f696a003"></script>
<script type="text/javascript" src="jsRule/system_fat/webrunFunctions.js?hash=1570995934"></script>
<script type="text/javascript" src="jsRule/system_fat/webrunRules.js?hash=13648834661708621672000"></script>
<script type="text/javascript" src="jsRule/system_fat/webrunMakerComponents.js?hash=16949273511708621670000"></script>
<script type="text/javascript" src="i18n/pt_BR.js?hash=288680576"></script>
<script type="text/javascript" src="i18n/translations_pt_BR.js"></script>
<script type="text/javascript" src="components/HTMLComponents.js?hash=28c58e5dd994bfba7b4655543b41eafc"></script>
<link rel="stylesheet" type="text/css" href="assets/bootstrap.min.css">
<link rel="stylesheet" type="text/css" href="assets/bootstrap-submenu.min.css">
<link rel="stylesheet" type="text/css" href="assets/fontawesome/css/all.min.css">
<link rel="stylesheet" type="text/css" href="assets/form.css?hash=b971b13f6bde3ee209005bd4dd53931f">
<link rel="stylesheet" type="text/css" href="assets/form.responsive.css?hash=ac969f61241c60402fb77e50a22000fa">
<link rel="stylesheet" type="text/css" href="assets/skins/Abas.css?hash=3f007102b43c0a92e40f98f4e53f7da1">
</head>
<body class="w-100" style="min-height: 100vh;" onload="formOnLoad(true); setFocusFormOnLoad(); defineOnUnload();">
<div id="loading"><div class="spinner-border text-primary" role="status"><span class="sr-only">...</span></div></div>
<script type="text/javascript">
document.addEventListener('DOMContentLoaded', function () {
//Realiza o design dos componentes carregados de forma async.
  formOnLoadComponents(true);
//Executa o evento Ao Entrar caso definido.
  formOnLoadAction();
});
var DECIMAL_POINT = ",";
var GROUPING_POINT = ".";
var DATE_PATTERN = "dd/MM/yyyy";
var TIME_PATTERN = "HH:mm:ss";
var DATE_TIME_PATTERN = "dd/MM/yyyy HH:mm:ss";
var richTextFound = false;
var mainform = window;
var mainframe = (opener != null) ? opener.mainframe : parent.mainframe;
var sysCode = "FAT";
var idForm = "3";
var formGUID = "{F75389C0-3525-4CE3-A27E-B819A59618EF}";
var isPopup = false;
var isDotNET = true;
var isTomcat7 = false;
var projectMode = "N";
var e_access = true;
const webrunBroadcast = new BroadcastChannel('webrun_channel_fat');
webrunLoadOnmessage();
mainform.webrunBroadcast = webrunBroadcast;
var navigationFixed = false;
var WEBRUN_CSRFTOKEN = "G78bgG2ACgoLOUqZvQ0A";
var isPrincipal = false;
var isLoginForm = true;
var loginForm = true;
parent.changeTitle("Harpix - Historico de Fat MEZ");
function defineOnUnload() {
  if (window.onunload) {
    window.formWindowOnUnload = window.onunload;
  }
  window.onunload = function(e) {
    if (window.formWindowOnUnload) {
      window.formWindowOnUnload(e);
    }
    formOnUnLoad(true);
    if (d.c_1051797) d.c_1051797 = null;
    if (d.c_1051798) d.c_1051798 = null;
    if (d.c_1051799) d.c_1051799 = null;
    if (d.c_1051795) d.c_1051795 = null;
    if (d.c_1051796) d.c_1051796 = null;
    if (d.c_1051802) d.c_1051802 = null;
    if (d.c_1051800) d.c_1051800 = null;
    if (makercontroller) makercontroller = null;
    if (d.ac && d.ac.flush) {
      d.ac.flush();
      d.ac = null;
    }
    if (d.t) d.t = null;
    if (d.n) d.n = null;
    if (d.p) d.p = null;
    if (d) d = null;
    clearReferences(document);
    window.onunload = function(e) {return false;}
  }
}
var anonymousAuthentication = true;
var loggedUserWithProfile = true;
</script>
<script type="text/javascript">
function formBeforeUpdate() {

}
function formBeforeInsert() {

}
function formBeforeDelete() {

}
function formAfterUpdate() {

}
function formAfterInsert() {

}
function formAfterDelete() {

}
function formOnNavigate() {
}
var pkeys = '';
var formrow = -1;
var hasdata = false;
var filter = false;
var edit = false;
var insert = false;
</script>
<iframe class="d-none" allowtransparency="true" name="WFRFormComands" src="nothing.html" width="0" height="0"></iframe>
<form class="w-100 m-0 d-flex flex-fill" name="WFRForm" method="post" action="form.do" target="WFRFormComands">
<input name="sys" type="hidden" value="FAT">
<input name="formID" type="hidden" value="3">
<input name="action" type="hidden" value="form">
<input name="param" type="hidden" value="post">
<input name="WEBRUN-CSRFTOKEN" type="hidden" value="G78bgG2ACgoLOUqZvQ0A">
<input name="goto" type="hidden" value="-1">
<input name="invisibleFields" type="hidden" value="">
<input name="storedProcedureName" type="hidden" value="">
<input name="storedProcedureParams" type="hidden" value="">
<div class="w-100 d-flex flex-column flex-fill" id="lay" style="width: 1024px; min-height: 100vh;">
<style type="text/css">
.tab-content{
 overflow: hidden !important;
}

#btnLogin, #btnLogin button {
    border-top-left-radius: 6%;
    border-bottom-left-radius: 6%;
   }


.btn {
 display:inline-block;
 font-weight:400;
 color:#f8f9fa;
 text-align:center;
 vertical-align:middle;
 cursor:pointer;
 -webkit-user-select:none;
 -moz-user-select:none;
 -ms-user-select:none;
 user-select:none;
 background-color:#0000;
 border:1px solid #0000;
 padding:.375rem .75rem;
 font-size:1rem;
 line-height:1.5;
 border-radius:.25rem;
 transition:color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out
}

.btn-outline-light {
 border-color:#f8f9fa !important;
}

.btn-login {
 animation:move 500ms !important;
 animation-delay:350ms !important;
 animation-fill-mode:backwards !important;
}

.text-white {
 color:#fff!important;
}

.float-right {
 float:right!important
}

.form-group,
 .form-label {
  margin-bottom:0
 } 

 .form-group,
.form-menu,
.form-action {
 position:absolute
}

.brand_logo_container {
    animation: fade 400ms;
    animation-delay: 600ms;
    animation-fill-mode: backwards;
}



</style>
<script type="text/javascript">
controller.addForm(3, '{F75389C0-3525-4CE3-A27E-B819A59618EF}');
if (isFormOpenInGroupBox()) {
  var parentGroupBox = getFormParentGroupBox();
  if (parentGroupBox) addFormToHierarchy(parentGroupBox.formID, idForm);
}
var d = document;
d.lay = d.getElementById('lay');
var makercontroller = new HTMLMakerController('FAT', 3);
var messagesAsAlert = false;
var securityVersion = "0";
var webrunVersion = "1.2.1.8 .NET";
function onloadWebrunComponents () {
d.n = new HTMLNavigationForm('FAT', 3, 2, 3);
d.n.developmentMode = false;
d.n.isEditable = false;
d.n.isModal = false;
d.n.responsive = true;
d.n.hideButtons = true;
d.n.visible = false;
d.n.design(d.lay);
d.n.setMainImages(1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1);
d.n.setEditImages(1, 1);
d.n.setIncludeImages(1, 1, 1);
d.ac = new HTMLAlert();
d.ac.hideImages = true;
d.ac.visible = false;
d.ac.design(d.lay);
d.t = new HTMLTabController('FAT', 3, 0, 0, 801, 613, true);d.t.showTabButtons = false;d.t.useReadOnlyDiv = false;
d.t.responsive = true;
d.t.horizontalCentered = false;
d.t.verticalCentered = false;
d.t.color = '';
d.t.dependences = new Array();
d.n.setTabController(d.t);
d.n.setAlertController(d.ac);
d.t.design(d.lay);
d.t.add('Cadastro');
d.c_1051797 = new HTMLContainer('FAT', 3, 1051797, 192, 66, 609, 435, '', '');
d.c_1051797.id = 'formLogin';
d.c_1051797.styleCss = '';
d.c_1051797.container = '';
d.c_1051797.classCss = 'form-group card bg-info m-auto pb-2 border-0 text-white shadow-lg';
d.c_1051797.zindex = 0;
d.c_1051797.design(d.t.getDiv(), false);
d.c_1051798 = new HTMLContainer('FAT', 3, 1051798, 0, 0, 609, 129, '', '');
d.c_1051798.id = 'MakerContainer3';
d.c_1051798.styleCss = '';
d.c_1051798.container = 'formLogin';
d.c_1051798.classCss = 'form-group bg-white no-border';
d.c_1051798.zindex = 1;
d.c_1051798.design(d.getElementById('formLogin'), false);
d.c_1051799 = new HTMLContainer('FAT', 3, 1051799, 64, 154, 489, 175, '', '');
d.c_1051799.id = 'inputsLogin';
d.c_1051799.styleCss = '';
d.c_1051799.container = 'formLogin';
d.c_1051799.classCss = 'form-group no-border';
d.c_1051799.zindex = 2;
d.c_1051799.design(d.getElementById('formLogin'), false);
d.c_1051802 = new HTMLButton('FAT', 3, 1051802, 464, 341, 89, 73, '<i class=\"fas fa-sign-in-alt d-block\"></i>Entrar', '');
d.c_1051802.onclick =  function() { return executeRule('FAT', 3, 'Template - Formulário de Login - Obter Dados e Efetuar Login', [1051800], [1051797, 1051798, 1051799, 1051802, 1051795, 1051796, 1051800], arguments);  };
d.c_1051802.id = 'btnLogin';
d.c_1051802.styleCss = '';
d.c_1051802.container = 'formLogin';
d.c_1051802.classCss = 'form-group btn btn-outline-light float-right text-white btn-login';
d.c_1051802.design(d.getElementById('formLogin'), false);
d.c_1051795 = new HTMLContainer('FAT', 3, 1051795, 224, 0, 137, 129, '', '');
d.c_1051795.id = 'MakerContainer5';
d.c_1051795.styleCss = '';
d.c_1051795.container = 'MakerContainer3';
d.c_1051795.classCss = 'form-group brand_logo_container rounded-circle bg-white mt-4 p-1 overflow-hidden';
d.c_1051795.zindex = 0;
d.c_1051795.design(d.getElementById('MakerContainer3'), false);
d.c_1051796 = new HTMLImage('FAT', 3, 1051796, 9, 5, 119, 119, '', 'openImageStreamFromGalery.do?sys=FAT&formID=3&guid=%7bB77C07AC-84EB-4CFE-B14B-A2BD83E9C5F2%7d', 3, false, false);
d.c_1051796.hasImage = true;
d.c_1051796.staticImage = true;
d.c_1051796.viewMode = 'Estender';
d.c_1051796.exhibitionType = 0;
d.c_1051796.zoomWidth = 0;
d.c_1051796.zoomHeight = 0;
d.c_1051796.md5 = '';
d.c_1051796.id = 'fotoEmpresa';
d.c_1051796.styleCss = '';
d.c_1051796.container = 'MakerContainer5';
d.c_1051796.zindex = 0;
d.c_1051796.design(d.getElementById('MakerContainer5'), false);
d.c_1051800 = new HTMLEdit('FAT', 3, 1051800, 40, 67, 393, 50, 'Digite aqui seu código ONS', '');
d.c_1051800.autocomplete = true;
d.c_1051800.classic = false;
d.c_1051800.onkeypress =  function() { return executeJSRule('FAT', 3, 'TemplateFormularioLoginAoLogar', [null, null, null, null, null, 1051800, null], false, arguments);  };
d.c_1051800.labelPosition = '0';
d.c_1051800.id = 'txtONS';
d.c_1051800.styleCss = '';
d.c_1051800.container = 'inputsLogin';
d.c_1051800.classCss = '';
d.c_1051800.zindex = 0;
d.c_1051800.design(d.getElementById('inputsLogin'), true);
if (window.makerFlowComponentsDesign) {
  while (makerFlowComponentsDesign.length > 0) {
    makerFlowComponentsDesign.shift()();
  }
}
if (window.containerComponentsDesign) {
  while (containerComponentsDesign.length > 0) {
    containerComponentsDesign.shift()();
  }
}
defineComponentDependences();
if (d.n.btFirst) d.n.btFirst.setEnabled(false);
if (d.n.btPrevious) d.n.btPrevious.setEnabled(false);
if (d.n.btNext) d.n.btNext.setEnabled(false);
if (d.n.btLast) d.n.btLast.setEnabled(false);
if (d.n.btDelete) d.n.btDelete.setEnabled(false);
if (d.n.btDefaultValues) d.n.btDefaultValues.setEnabled(false);
d.ac.showFilter(false);
}
function formOnLoadAction() {
  bootstrapInitTooltip('[data-toggle="tooltip"]');
  controller.sortOrderTab();
  executeJSRule('FAT', 3, 'TemplateFormularioLoginAoEntrar', [], false, arguments);
}
function showErrors() {
}
function formOnLoadComponents (load) {
  if (load) onloadWebrunComponents();
}
function formOnLoad(load) {
  controller.onFormLoadAction();
  formOnNavigate();
  if (d.hasRuleErrors) d.hasRuleErrors = false;
  if (d.n.editCancel) d.n.editCancel = false;
  var preloaderElement = d.getElementById("loading");
  if (preloaderElement) preloaderElement.style.display = "none";
}
function formOnUnLoad(load) {
  EventCache.flush();
  controller.flush();
  if (mainform.isPrincipal) closeFormHierarchy(mainSystemFrame.formId);
}
function formOnUnLoadAction() {
  if (isFormOpenInGroupBox()) {
    try {
      closeFloatingFormChilds(idForm);
      removeFormFromHierarchy(idForm);
    } catch (e) { }
  }

  var d = document;
}
function executeFromActionScript(ruleName, ruleParams, isServerRule) {
  if(isServerRule) {
    return executeSyncJavaRule(sysCode, idForm, ruleName, ruleParams);
  } else {
    return executeJSRuleNoField(sysCode, idForm, ruleName, ruleParams, true)
  }
}
addKeyEvent();
</script>
</div>
</form>
<div id="messageDIV" style="position:absolute; left:0px; top:0px; width:150px; height:18px; z-index:1001; visibility: hidden;"></div>
</body>
</html>
