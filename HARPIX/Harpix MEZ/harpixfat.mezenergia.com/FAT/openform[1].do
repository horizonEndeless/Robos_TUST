<!DOCTYPE html>
<html class="w-100 overflow-sm-hidden">
<head>
<meta charset="ISO-8859-1">
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Abas - Formul&#225;rio Principal</title>
<script type="text/javascript">
var orderTab = [1051804, 1051806, 1051814, 1051889, 1051813, 1051805, 1051809, 1051817, 1051810, 1051811, 1051808, 1051812, 1051807, 1051815, 1051816];
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
var idForm = "500000435";
var formGUID = "{08DD8F12-E9DF-4047-99CE-E0F95372026F}";
var isPopup = false;
var isDotNET = true;
var isTomcat7 = false;
var projectMode = "N";
var e_access = false;
const webrunBroadcast = new BroadcastChannel('webrun_channel_fat');
webrunLoadOnmessage();
mainform.webrunBroadcast = webrunBroadcast;
var navigationFixed = false;
var WEBRUN_CSRFTOKEN = "AFBV7tGSvwy2uM8NDWBz";
var isPrincipal = true;
var principal = $mainform();
var isLoginForm = false;
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
    if (d.c_1051804) d.c_1051804 = null;
    if (d.c_1051806) d.c_1051806 = null;
    if (d.c_1051814) d.c_1051814 = null;
    if (d.c_1051889) d.c_1051889 = null;
    if (d.c_1051813) d.c_1051813 = null;
    if (d.c_1051805) d.c_1051805 = null;
    if (d.c_1051809) d.c_1051809 = null;
    if (d.c_1051817) d.c_1051817 = null;
    if (d.c_1051810) d.c_1051810 = null;
    if (d.c_1051811) d.c_1051811 = null;
    if (d.c_1051808) d.c_1051808 = null;
    if (d.c_1051812) d.c_1051812 = null;
    if (d.c_1051807) d.c_1051807 = null;
    if (d.c_1051815) d.c_1051815 = null;
    if (d.c_1051816) d.c_1051816 = null;
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
<input name="formID" type="hidden" value="500000435">
<input name="action" type="hidden" value="form">
<input name="param" type="hidden" value="post">
<input name="WEBRUN-CSRFTOKEN" type="hidden" value="AFBV7tGSvwy2uM8NDWBz">
<input name="goto" type="hidden" value="-1">
<input name="invisibleFields" type="hidden" value="">
<input name="storedProcedureName" type="hidden" value="">
<input name="storedProcedureParams" type="hidden" value="">
<div class="w-100 d-flex flex-column flex-fill" id="lay" style="width: 1044px; min-height: 100vh;">
<style type="text/css">
.tab-content{
 overflow: hidden !important;
}

#imgLogoContainer {
 left: 43px !important;
 width: 185px !important;
}

.dadosTop:hover {
  box-shadow: 0px 2px 12px -5px;
  transform: translate3d(-3px, 0, 0);
}

#Aba{
 left: 0% !important; 
 width: 99% !important;
}

.menu-collapse-button {
 display: inline-flex !important; 
}

#MenuLateralCosmo,
  .menu-collapse-button {
    top: 0.8rem !important;
  }

  #MenuLateralCosmoPrincipal,
  #MenuLateralCosmo {
    width: auto !important;    
    
  }

.form-menu.menu-collapse.menu-align-left:not(.show) {
    left: -100% !important;
}

.form-menu.menu-collapse {
    transition: all .5s ease;
    }

.form-menu.menu-collapse.menu-vertical {
    padding: 0.5rem;
}

.form-menu.menu-collapse.menu-vertical:not(.menu-with-search-top) {
    padding-top: 3.5rem;
  }

  .form-menu.menu-collapse.menu-vertical.menu-align-top .menu-search.menu-search-top .input-group,
  .form-menu.menu-collapse.menu-vertical.menu-align-left .menu-search.menu-search-top .input-group {
    padding-left: 3rem;
    height: 2.5rem;
  }

  .form-menu.menu-collapse.menu-vertical.menu-align-right .menu-search.menu-search-top .input-group {
    padding-right: 3rem;
    height: 2.5rem;
  }

  .form-menu.menu-collapse.menu-vertical.menu-align-top .menu-search.menu-search-top .input-group *,
  .form-menu.menu-collapse.menu-vertical.menu-align-left .menu-search.menu-search-top .input-group * {
    height: 100%;
  }

</style>
<script type="text/javascript">
controller.addForm(500000435, '{08DD8F12-E9DF-4047-99CE-E0F95372026F}');
if (isFormOpenInGroupBox()) {
  var parentGroupBox = getFormParentGroupBox();
  if (parentGroupBox) addFormToHierarchy(parentGroupBox.formID, idForm);
}
var d = document;
d.lay = d.getElementById('lay');
var makercontroller = new HTMLMakerController('FAT', 500000435);
var messagesAsAlert = false;
var securityVersion = "0";
var webrunVersion = "1.2.1.8 .NET";
function onloadWebrunComponents () {
d.n = new HTMLNavigationForm('FAT', 500000435, 2, 3);
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
d.t = new HTMLTabController('FAT', 500000435, 0, 0, 1022, 665, true);d.t.showTabButtons = false;d.t.useReadOnlyDiv = false;
d.t.responsive = true;
d.t.horizontalCentered = false;
d.t.verticalCentered = false;
d.t.color = '';
d.t.dependences = new Array();
d.n.setTabController(d.t);
d.n.setAlertController(d.ac);
d.t.design(d.lay);
d.t.add('Cadastro');
d.c_1051804 = new HTMLContainer('FAT', 500000435, 1051804, 0, 0, 1022, 80, '', '');
d.c_1051804.id = 'topoCosmo';
d.c_1051804.styleCss = '';
d.c_1051804.container = '';
d.c_1051804.classCss = 'shadow bg-info position-fixed w-100';
d.c_1051804.zindex = 2;
d.c_1051804.design(d.t.getDiv(), false);
d.c_1051806 = new HTMLContainer('FAT', 500000435, 1051806, 808, 24, 121, 33, '', '');
d.c_1051806.id = 'IconButtonContainer';
d.c_1051806.styleCss = '';
d.c_1051806.container = '';
d.c_1051806.classCss = 'form-group position-fixed';
d.c_1051806.zindex = 3;
d.c_1051806.design(d.t.getDiv(), false);
d.c_1051814 = new HTMLContainer('FAT', 500000435, 1051814, 960, 79, 62, 79, '', '');
d.c_1051814.id = 'MakerContainer6';
d.c_1051814.styleCss = '';
d.c_1051814.container = '';
d.c_1051814.classCss = 'form-group user-button d-flex justify-content-end position-fixed fixed-height';
d.c_1051814.zindex = 6;
d.c_1051814.design(d.t.getDiv(), false);
d.c_1051816 = new HTMLMakerFlowComponent('FAT', 500000435, 1051816, 232, 81, 713, 497, '', '', '');
d.c_1051816.Desdocar = 'True';
d.c_1051816.Aba = '01-Cadastro';
d.c_1051816.Dica = '';
d.c_1051816.ClasseComponente = 'Aba';
d.c_1051816.Codigo = '1051816';
d.c_1051816.Ordem = '1';
d.c_1051816.Altura = '497';
d.c_1051816.autoAjuste = '0';
d.c_1051816.Tamanho = '713';
d.c_1051816.Tabular = 'False';
d.c_1051816.AbaResponsiva = 'false';
d.c_1051816.Container = '';
d.c_1051816.FecharAba = 'true';
d.c_1051816.Tabulacao = '2';
d.c_1051816.Categoria = 'Adicionais';
d.c_1051816.Habilitado = 'True';
d.c_1051816.PosicaoY = '81';
d.c_1051816.PosicaoX = '232';
d.c_1051816.Acessivel = '1';
d.c_1051816.ListaDeFormularios = '';
d.c_1051816.Nome = 'Aba';
d.c_1051816.Visivel = 'True';
d.c_1051816.id = 'Aba';
d.c_1051816.styleCss = '';
d.c_1051816.container = '';
d.c_1051816.zindex = 1;
d.c_1051816.design('Aba - Iniciar Componente', new Map().add('Desdocar','True').add('Aba','01-Cadastro').add('Dica','').add('ClasseComponente','Aba').add('Codigo','1051816').add('Ordem','1').add('Altura','497').add('autoAjuste','0').add('Tamanho','713').add('Tabular','False').add('AbaResponsiva','false').add('Container','').add('FecharAba','true').add('Tabulacao','2').add('Categoria','Adicionais').add('Habilitado','True').add('PosicaoY','81').add('PosicaoX','232').add('Acessivel','1').add('ListaDeFormularios','').add('Nome','Aba').add('Visivel','True'));
d.c_1051808 = new HTMLMakerFlowComponent('FAT', 500000435, 1051808, 4, 82, 224, 583, '', '', '');
d.c_1051808.Aba = '01-Cadastro';
d.c_1051808.PlaceHolder = 'Buscar no menu';
d.c_1051808.Tamanho = '224';
d.c_1051808.Tabular = 'False';
d.c_1051808.Container = '';
d.c_1051808.Categoria = 'Maker 3';
d.c_1051808.PosicaoPesquisa = 'T';
d.c_1051808.Alinhamento = 'L';
d.c_1051808.Habilitado = 'True';
d.c_1051808.PesquisaMenu = 'true';
d.c_1051808.Nome = 'MenuLateralCosmo';
d.c_1051808.AutoRetrair = 'true';
d.c_1051808.Visivel = 'True';
d.c_1051808.AoSoltarAtalho = new Map().add('Destino','1').add('Nome','TemplateAdicionarAtalhoAoFabContainer').add('Entrada','atalho=');
d.c_1051808.Dica = '';
d.c_1051808.ClasseComponente = 'Menu';
d.c_1051808.Codigo = '1051808';
d.c_1051808.MenuAbas = 'Aba';
d.c_1051808.Ordem = '7';
d.c_1051808.Altura = '583';
d.c_1051808.XMLMenu = 'eJxVkVFvgyAQxz8NT4RFQQs8gmBqUmWx3ZLtzbR2M+lqonbZvv2Oim3HA8n978f97w7EMsTyn68T\n/m6HsevPiBlEafwUwY3b874/dOePWezGngiRShJDAK8QsyhSiGW1czu8W9vSzuA1HXKlrV5w5kxI\nJTHnkt2BSAJj7Dari+dd4SqQ1904oZwN3b7HhxbnzXQZmhEwRPP/5K1AkbkKTDauXhpgMVdUCz/E\ntni3y1Q0na2PzYiPDfkEq374nWv7Io9Fc1eXEKeRPwnjMxVUjyzga7Et9AY87DRc2hm7azestsq4\navN2tT+NAXxQgcTh+JmMl7jWSuvEaE2EZSuSKMmJklISocQqonm6yqhA3IQZzG3xEPndLx0EyX8V\nSH+r6Xto\n';
d.c_1051808.Orientacao = 'V';
d.c_1051808.Tabulacao = '1';
d.c_1051808.PosicaoY = '82';
d.c_1051808.PosicaoX = '4';
d.c_1051808.MenuLegado = 'false';
d.c_1051808.id = 'MenuLateralCosmo';
d.c_1051808.styleCss = '';
d.c_1051808.container = '';
d.c_1051808.zindex = 7;
d.c_1051808.design('Menu - Iniciar Componente', new Map().add('Aba','01-Cadastro').add('PlaceHolder','Buscar no menu').add('Tamanho','224').add('Tabular','False').add('Container','').add('Categoria','Maker 3').add('PosicaoPesquisa','T').add('Alinhamento','L').add('Habilitado','True').add('PesquisaMenu','true').add('Nome','MenuLateralCosmo').add('AutoRetrair','true').add('Visivel','True').add('Ao Soltar Atalho',new Map().add('Destino','1').add('Nome','TemplateAdicionarAtalhoAoFabContainer').add('Entrada','atalho=')).add('Dica','').add('ClasseComponente','Menu').add('Codigo','1051808').add('MenuAbas','Aba').add('Ordem','7').add('Altura','583').add('XMLMenu','eJxVkVFvgyAQxz8NT4RFQQs8gmBqUmWx3ZLtzbR2M+lqonbZvv2Oim3HA8n978f97w7EMsTyn68T\n/m6HsevPiBlEafwUwY3b874/dOePWezGngiRShJDAK8QsyhSiGW1czu8W9vSzuA1HXKlrV5w5kxI\nJTHnkt2BSAJj7Dari+dd4SqQ1904oZwN3b7HhxbnzXQZmhEwRPP/5K1AkbkKTDauXhpgMVdUCz/E\ntni3y1Q0na2PzYiPDfkEq374nWv7Io9Fc1eXEKeRPwnjMxVUjyzga7Et9AY87DRc2hm7azestsq4\navN2tT+NAXxQgcTh+JmMl7jWSuvEaE2EZSuSKMmJklISocQqonm6yqhA3IQZzG3xEPndLx0EyX8V\nSH+r6Xto\n').add('Orientacao','V').add('Tabulacao','1').add('PosicaoY','82').add('PosicaoX','4').add('MenuLegado','false'));
d.c_1051889 = new HTMLImage('FAT', 500000435, 1051889, 0, 96, 1017, 513, '', 'openImageStreamFromGalery.do?sys=FAT&formID=500000435&guid=%7b13FBA7C4-7932-40C8-BAA2-B4C85B6362CF%7d', 3, false, false);
d.c_1051889.hasImage = true;
d.c_1051889.staticImage = true;
d.c_1051889.viewMode = 'Estender';
d.c_1051889.exhibitionType = 0;
d.c_1051889.zoomWidth = 0;
d.c_1051889.zoomHeight = 0;
d.c_1051889.md5 = '';
d.c_1051889.id = 'MakerImage2';
d.c_1051889.styleCss = '';
d.c_1051889.container = '';
d.c_1051889.zindex = 0;
d.c_1051889.design(d.t.getDiv(), false);
d.c_1051813 = new HTMLContainer('FAT', 500000435, 1051813, 910, 398, 97, 185, '', '');
d.c_1051813.visible = false;
d.c_1051813.id = 'atalhosListaContainer';
d.c_1051813.styleCss = '';
d.c_1051813.container = '';
d.c_1051813.classCss = 'collapse position-fixed';
d.c_1051813.zindex = 4;
d.c_1051813.design(d.t.getDiv(), false);
d.c_1051812 = new HTMLButton('FAT', 500000435, 1051812, 928, 584, 64, 64, '<i class=\"fas fa-reply-all fa-lg text-white\"></i><i class=\"fas fa-times fa-lg text-white\"></i><i class=\"fas fa-chevron-left fa-lg text-white\"></i>', '');
d.c_1051812.onclick =  function() { return executeJSRule('FAT', 500000435, 'TemplateAbrirContainerDeAtalhos', [], false, arguments);  };
d.c_1051812.visible = false;
d.c_1051812.enabled = false;
d.c_1051812.id = 'atalhosFAB';
d.c_1051812.styleCss = '';
d.c_1051812.container = '';
d.c_1051812.classCss = 'position-fixed m-0 rounded-circle shadow btn-dark collapsed';
d.c_1051812.design(d.t.getDiv(), false);
d.c_1051805 = new HTMLContainer('FAT', 500000435, 1051805, 10, 4, 191, 73, '', '');
d.c_1051805.onclick =  function() { return executeJSRule('FAT', 500000435, 'AbasFormularioPrincipalAbrirSiteDoHarpix', [], false, arguments);  };
d.c_1051805.id = 'imgLogoContainer';
d.c_1051805.styleCss = '';
d.c_1051805.container = 'topoCosmo';
d.c_1051805.classCss = 'form-group d-none d-sm-block border-right border-light';
d.c_1051805.zindex = 0;
d.c_1051805.design(d.getElementById('topoCosmo'), false);
d.c_1051809 = new HTMLContainer('FAT', 500000435, 1051809, 936, 5, 82, 71, '', '');
d.c_1051809.id = 'userImageContainer';
d.c_1051809.styleCss = '';
d.c_1051809.container = 'topoCosmo';
d.c_1051809.classCss = 'form-group border-left border-light d-flex align-items-center justify-content-center';
d.c_1051809.zindex = 1;
d.c_1051809.design(d.getElementById('topoCosmo'), false);
d.c_1051817 = new HTMLImage('FAT', 500000435, 1051817, 18, 8, 159, 57, '', 'openImageStreamFromGalery.do?sys=FAT&formID=500000435&guid=%7bE6661B1F-54AD-4834-BDCA-8F463DAE745F%7d', 3, false, false);
d.c_1051817.hasImage = true;
d.c_1051817.staticImage = true;
d.c_1051817.viewMode = 'Estender';
d.c_1051817.exhibitionType = 0;
d.c_1051817.zoomWidth = 0;
d.c_1051817.zoomHeight = 0;
d.c_1051817.md5 = '';
d.c_1051817.onclick =  function() { return executeJSRule('FAT', 500000435, 'AbasFormularioPrincipalAbrirSiteDoHarpix', [], false, arguments);  };
d.c_1051817.id = 'imgLogo';
d.c_1051817.styleCss = '';
d.c_1051817.container = 'imgLogoContainer';
d.c_1051817.zindex = 0;
d.c_1051817.design(d.getElementById('imgLogoContainer'), false);
d.c_1051810 = new HTMLImage('FAT', 500000435, 1051810, 20, 3, 45, 45, '', 'openImageStreamFromGalery.do?sys=FAT&formID=500000435&guid=%7bDF91D13C-E163-4160-B487-31E8CFB2F348%7d', 3, false, false);
d.c_1051810.hasImage = true;
d.c_1051810.staticImage = true;
d.c_1051810.viewMode = 'Estender';
d.c_1051810.exhibitionType = 0;
d.c_1051810.zoomWidth = 0;
d.c_1051810.zoomHeight = 0;
d.c_1051810.md5 = '';
d.c_1051810.id = 'userImage';
d.c_1051810.styleCss = '';
d.c_1051810.container = 'userImageContainer';
d.c_1051810.zindex = 0;
d.c_1051810.design(d.getElementById('userImageContainer'), false);
d.c_1051811 = new HTMLLabel('FAT', 500000435, 1051811, 5, 51, 73, 21, 'Usuário');
d.c_1051811.horizontalAlignment = 'center';
d.c_1051811.verticalAlignment = 'middle';
d.c_1051811.wrap = true;
d.c_1051811.id = 'userName';
d.c_1051811.styleCss = '';
d.c_1051811.container = 'userImageContainer';
d.c_1051811.classCss = 'text-white';
d.c_1051811.zindex = 1;
d.c_1051811.design(d.getElementById('userImageContainer'), false);
d.c_1051807 = new HTMLMakerFlowComponent('FAT', 500000435, 1051807, 52, -3, 53, 36, '', '', '');
d.c_1051807.Aba = '01-Cadastro';
d.c_1051807.PlaceHolder = 'Buscar no menu';
d.c_1051807.Tamanho = '53';
d.c_1051807.Tabular = 'False';
d.c_1051807.Container = 'IconButtonContainer';
d.c_1051807.Categoria = 'Maker 3';
d.c_1051807.PosicaoPesquisa = 'L';
d.c_1051807.Habilitado = 'True';
d.c_1051807.PesquisaMenu = 'false';
d.c_1051807.Nome = 'icons';
d.c_1051807.Visivel = 'True';
d.c_1051807.AoSoltarAtalho = new Map().add('Destino','1').add('Nome','TemplateAdicionarAtalhoAoFabContainer').add('Entrada','atalho=');
d.c_1051807.Dica = '';
d.c_1051807.ClasseComponente = 'Menu';
d.c_1051807.Codigo = '1051807';
d.c_1051807.MenuAbas = '';
d.c_1051807.Ordem = '0';
d.c_1051807.AoClicar = new Map().add('Destino','1').add('Nome','TemplateAoClicarNoItemDoMenuAcao').add('Entrada','evento=');
d.c_1051807.Altura = '36';
d.c_1051807.XMLMenu = 'eJytlU1vozAQhn+NT4gKQyBwjAjJRkqgG9JLby5Msl4RHNmmyvbXdyhdaKRdp0hcEH49nnce+WOI\nFxNvdT1X1itIxUVNvCVxXfrg4NeCuhAlr0+dyJWww9CPbIoDXEW8hDgL4sX7LDtYhx/JLukCK376\npT9iPgN2Sfpkxdnyc56G4TyY0yHCiTBomeTxfvN42GQpymvZXIRCmbir25l+wSbOUsy6zfZd2rQt\nOd88J8MQw49MWUdmNwr5unTtur60RfwPw17sYlBpCf6LE0SR74ZGnCfVkIRKPiUSK0sJStkFk6WJ\nDL3Z4DyazXV8z8i2zdbTQR15BTartAmoNxzHMqM+Ne9SXkh+0Vb+czsdUMk0e2EKTEDJFYpGM9n5\n9/bj8Dw3cGaRkW8PeFYknJi0cq40nNl0nOpPXZgYB+8b65GMXuA65tO4E6WwUiHPrJr29TDBtaZf\nPcdR+e6cBsF9qjVIqDVMi2VrbjybrfON8Ti2iIaB499ne5TiN2gxHRt2rrtcN6bjuEKK76L5tsWi\nPvJTI/G24S9cycqHCZ//F3jjuH1FI1+NoEMZH1UIUIuSF9jqGf9OS/grtU0epXf9gRw3\n';
d.c_1051807.Orientacao = 'H';
d.c_1051807.Tabulacao = '1';
d.c_1051807.PosicaoY = '-3';
d.c_1051807.PosicaoX = '52';
d.c_1051807.MenuLegado = 'false';
d.c_1051807.onclick =  function() { return executeJSRule('FAT', 500000435, 'TemplateAoClicarNoItemDoMenuAcao', [null], false, arguments);  };
d.c_1051807.id = 'icons';
d.c_1051807.styleCss = '';
d.c_1051807.container = 'IconButtonContainer';
d.c_1051807.zindex = 0;
d.c_1051807.design('Menu - Iniciar Componente', new Map().add('Aba','01-Cadastro').add('PlaceHolder','Buscar no menu').add('Tamanho','53').add('Tabular','False').add('Container','IconButtonContainer').add('Categoria','Maker 3').add('PosicaoPesquisa','L').add('Habilitado','True').add('PesquisaMenu','false').add('Nome','icons').add('Visivel','True').add('Ao Soltar Atalho',new Map().add('Destino','1').add('Nome','TemplateAdicionarAtalhoAoFabContainer').add('Entrada','atalho=')).add('Dica','').add('ClasseComponente','Menu').add('Codigo','1051807').add('MenuAbas','').add('Ordem','0').add('Ao Clicar',new Map().add('Destino','1').add('Nome','TemplateAoClicarNoItemDoMenuAcao').add('Entrada','evento=')).add('Altura','36').add('XMLMenu','eJytlU1vozAQhn+NT4gKQyBwjAjJRkqgG9JLby5Msl4RHNmmyvbXdyhdaKRdp0hcEH49nnce+WOI\nFxNvdT1X1itIxUVNvCVxXfrg4NeCuhAlr0+dyJWww9CPbIoDXEW8hDgL4sX7LDtYhx/JLukCK376\npT9iPgN2Sfpkxdnyc56G4TyY0yHCiTBomeTxfvN42GQpymvZXIRCmbir25l+wSbOUsy6zfZd2rQt\nOd88J8MQw49MWUdmNwr5unTtur60RfwPw17sYlBpCf6LE0SR74ZGnCfVkIRKPiUSK0sJStkFk6WJ\nDL3Z4DyazXV8z8i2zdbTQR15BTartAmoNxzHMqM+Ne9SXkh+0Vb+czsdUMk0e2EKTEDJFYpGM9n5\n9/bj8Dw3cGaRkW8PeFYknJi0cq40nNl0nOpPXZgYB+8b65GMXuA65tO4E6WwUiHPrJr29TDBtaZf\nPcdR+e6cBsF9qjVIqDVMi2VrbjybrfON8Ti2iIaB499ne5TiN2gxHRt2rrtcN6bjuEKK76L5tsWi\nPvJTI/G24S9cycqHCZ//F3jjuH1FI1+NoEMZH1UIUIuSF9jqGf9OS/grtU0epXf9gRw3\n').add('Orientacao','H').add('Tabulacao','1').add('PosicaoY','-3').add('PosicaoX','52').add('MenuLegado','false'));
d.c_1051815 = new HTMLMakerFlowComponent('FAT', 500000435, 1051815, 2, 5, 57, 47, '', '', '');
d.c_1051815.Aba = '01-Cadastro';
d.c_1051815.Dica = '';
d.c_1051815.ClasseComponente = 'Menu';
d.c_1051815.PlaceHolder = 'Buscar no menu';
d.c_1051815.Codigo = '1051815';
d.c_1051815.MenuAbas = '';
d.c_1051815.Ordem = '0';
d.c_1051815.Altura = '47';
d.c_1051815.Tamanho = '57';
d.c_1051815.XMLMenu = 'eJxVkF0LgyAUhn+NV+JwSVCXYY4FK0cfN7uTrTWhJWiN/fydZjV2I/ic57y8ihhH7PB+9vjVWqfN\ngFiKgmC/o3Didriamx46D7UzJIrCmOzhAluICUQTxHgpZY3ro8iFF3vdPcavswi5KBrMZbrMI0oZ\nC34CjcFJRcXL7FxnsgBcKW0BouDwzzc947KAyJMsfeZct8ouYu0f+vi7cviuiNPdQMw0EtWPPnbe\n3/olfIlP+rG1yjZuUlYbb25D7wKZn7N2WdD8BYA+kB9WJA==\n';
d.c_1051815.Orientacao = 'H';
d.c_1051815.Tabular = 'False';
d.c_1051815.Container = 'MakerContainer6';
d.c_1051815.Tabulacao = '1';
d.c_1051815.Categoria = 'Maker 3';
d.c_1051815.PosicaoPesquisa = 'L';
d.c_1051815.Habilitado = 'True';
d.c_1051815.PesquisaMenu = 'false';
d.c_1051815.PosicaoY = '5';
d.c_1051815.PosicaoX = '2';
d.c_1051815.MenuLegado = 'false';
d.c_1051815.Nome = 'optionsUser';
d.c_1051815.Visivel = 'True';
d.c_1051815.id = 'optionsUser';
d.c_1051815.styleCss = '';
d.c_1051815.container = 'MakerContainer6';
d.c_1051815.zindex = 0;
d.c_1051815.design('Menu - Iniciar Componente', new Map().add('Aba','01-Cadastro').add('Dica','').add('ClasseComponente','Menu').add('PlaceHolder','Buscar no menu').add('Codigo','1051815').add('MenuAbas','').add('Ordem','0').add('Altura','47').add('Tamanho','57').add('XMLMenu','eJxVkF0LgyAUhn+NV+JwSVCXYY4FK0cfN7uTrTWhJWiN/fydZjV2I/ic57y8ihhH7PB+9vjVWqfN\ngFiKgmC/o3Didriamx46D7UzJIrCmOzhAluICUQTxHgpZY3ro8iFF3vdPcavswi5KBrMZbrMI0oZ\nC34CjcFJRcXL7FxnsgBcKW0BouDwzzc947KAyJMsfeZct8ouYu0f+vi7cviuiNPdQMw0EtWPPnbe\n3/olfIlP+rG1yjZuUlYbb25D7wKZn7N2WdD8BYA+kB9WJA==\n').add('Orientacao','H').add('Tabular','False').add('Container','MakerContainer6').add('Tabulacao','1').add('Categoria','Maker 3').add('PosicaoPesquisa','L').add('Habilitado','True').add('PesquisaMenu','false').add('PosicaoY','5').add('PosicaoX','2').add('MenuLegado','false').add('Nome','optionsUser').add('Visivel','True'));
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
  executeJSRule('FAT', 500000435, 'AbasFormularioPrincipalAoEntrarCnt', [], false, arguments);
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
