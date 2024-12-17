
function ComponenteEditavel(componente){$c(componente).div.style.zIndex=100000}
function OpenURLOnNewWindow(pURL,pWindowName,pWindowProperties){try{MM_openBrWindow(pURL,pWindowName,pWindowProperties);}catch(e){}}
function OpenURLOnNewWindow_copy(pURL,pWindowName,pWindowProperties){try{MM_openBrWindow(pURL,pWindowName,pWindowProperties);}catch(e){}}
function cmsOpenerWindowRefreshComponent(form,componentName,allWindows){var first=true;var current=top;while(((caller=getOpenerWindow(current))!=null)&&(allWindows===true||first)){first=false;if(!caller.mainform||isNullable(caller.mainform.sysCode)){return;}
var mainform=caller.$mainform();if(mainform){var component=mainform.$c(componentName,form);if(component&&component.refresh){component.refresh();return;}}
current=caller;}}
function ebfAccordionOpenForm(section,form){if(section&&form){let elemento=document.getElementById(section);let url="form"+PAGES_EXTENSION+"?";url+="sys="+sysCode;url+="&action=openform&formID="+URLEncode(form,"GET");url+="&align=0&mode=-1&goto=-1&filter=&scrolling=false";if(elemento.children[0]){elemento.children[0].src=url;}else{let iframe=document.createElement("iframe");iframe.className="w-100 h-100 border-0 m-0";iframe.style.outline="0";iframe.src=url;elemento.appendChild(iframe);}}}
function ebfAccordionOpenURL(section,url){let elemento=document.getElementById(section);if(elemento.children[0]){elemento.children[0].src=url;}else{let iframe=document.createElement("iframe");iframe.className="w-100 h-100 border-0 m-0";iframe.style.outline="0";iframe.src=url;elemento.appendChild(iframe);}}
function ebfAccordionSetContent(section,content){if(section&&content){section=document.getElementById(section);if(section)
section.innerHTML=content;}}
function ebfActionExecute(action){switch(action.trim().toLowerCase()){case"incluir":{ebfFormInsertMode();break;}
case"alterar":{ebfFormEditMode();break;}
case"excluir":{ebfNavDeleteCurrentRecord();break;}
case"gravar":{ebfNavEditSaveRecord();break;}
case"gravarmais":{ebfNavIncludeMoreSaveRecord();break;}
case"primeiroreg":{ebfNavFirstRecord();break;}
case"anteriorreg":{ebfNavPreviousRecord();break;}
case"proximoreg":{ebfNavNextRecord();break;}
case"ultimoreg":{ebfNavLastRecord();break;}
case"cancelar":{if(ebfFormIsInEditMode())ebfNavEditCancel();else if(ebfFormIsInInsertMode())ebfNavIncludeCancel();break;}
case"grupos":{IframeTransporter("executeFunction.do?action=executeFunction&sys="+ebfGetFullSystemID()+"&function=ebfFormOpenFormGroup");break;}
case"usuarios":{IframeTransporter("executeFunction.do?action=executeFunction&sys="+ebfGetFullSystemID()+"&function=ebfFormOpenFormUser");break;}
case"log":{openFormLog(ebfGetFullSystemID(),'','Log','',2);break;}
case"alterarsenha":{IframeTransporter("executeFunction.do?action=executeFunction&sys="+ebfGetFullSystemID()+"&function=ebfFormOpenFormPassword");break;}
case"executarscriptsql":{openWFRSQLScriptExecute(ebfGetFullSystemID());break;}
case"recarregarsistema":{shortcutReloadSystem(ebfGetFullSystemID());break;}
case"alterarusuario":{ebfSystemChangeUser();break;}
case"sair":{ebfSystemExit();break;}
case"modonormal":{ebfMenuChangeMode('n');break;}
case"modogerente":{ebfMenuChangeMode('p');break;}
case"modoprojeto":{ebfMenuChangeMode('d');break;}
case"configurarconexoesadicionais":{openWFRConfigureSubconnections(ebfGetFullSystemID());break;}}}
function ebfActionNew(tab,name,posX,posY,height,width,urlImage,urlImageClick,urlImageOver,guidImage,guidImageClick,guidImageOver,modeAccessible,defaultAction,title,enable,compContainer){let code=getCodComponent();let component=new HTMLActionButton(ebfGetSystemID(),ebfGetFormID(),code,posX,posY,width,height,"","");component.id=name;component.zindex=3;component.loadComponentTime=0;component.Aba=tab;component.AcoesPreDefinida=defaultAction;component.Tamanho=width;component.Image=guidImage;component.Container=compContainer;component.Categoria='Maker 3';component.Habilitado=enable;component.URLImageMouseOver=urlImageOver;component.URLImageOnClick=urlImageClick;component.Acessivel=modeAccessible;component.Nome=name;component.Visivel='True';component.Dica=title;component.ClasseComponente='Acao';component.ImageMouseOver=guidImageOver;component.URLImage=urlImage;component.Altura=height;component.ImageOnClick=guidImageClick;component.PosicaoY=posX;component.PosicaoX=posY;let container=$mainform().d.t.getTabByName(tab);if(!container){d.t.add(tab);container=$mainform().d.t.getTabByName(tab);}
if(compContainer){compContainer=document.getElementById(compContainer);component.design(compContainer,true);}else{component.design(container.div,true);}}
function ebfActionSetImage(name,urlImage,event){let component=$c(name);if(!component){interactionError(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",name));return false;}
let isGUID=urlImage.startsWith("{");event=event?event:"";switch(event.toLowerCase()){case'ao clicar':if(isGUID){component.ImageOnClick=urlImage;}else{component.URLImageOnClick=urlImage;}
break;case'ao passar o mouse':if(isGUID){component.ImageMouseOver=urlImage;}else{component.URLImageMouseOver=urlImage;}
break;default:if(isGUID){component.Image=urlImage;}else{component.URLImage=urlImage;}
break;}
component.updateImage();}
function ebfAddChild(tree,parentElement,description){return tree.addChild(parentElement,description);}
function ebfAddEventForm(evento,fluxo,lista){if(evento&&fluxo){fluxo=reduceVariable(fluxo);var w=mainform;if(w.addEventListener){w.addEventListener(evento,function(){return ebfFlowExecute(fluxo,lista);},false);}else{if(w.attachEvent){w.attachEvent(evento,function(){return ebfFlowExecute(fluxo,lista);});}}}}
function ebfAlertMessage(msg){alert(msg);}
function ebfAppBringToFront(){alert('Função disponível apenas no MakerMobile');}
function stoneSDKCreateTransaction(){alert('Função disponível apenas no MakerMobile');}
function ebfAppend(){var value="";if(existArgs(arguments)){for(var i=0;i<arguments.length;i++){if(arguments[i]==null)arguments[i]='';var temp=arguments[i].toString();value+=temp;}}
return value;}
function ebfArredondaDecimal(value,decimalQtt,abnt){if(abnt){var floatValue=parseFloat(value.toString().replaceAll(",","."));if(parseInt(value)===floatValue){return floatValue;}else{return round_abnt(floatValue,decimalQtt);}}else{value=parseNumeric(value);var factor=Math.pow(10,parseNumeric(decimalQtt));value*=factor;value=Math.round(value);value/=factor;}
return value;}
function round_abnt(nValor,nDecimais){var nRetorno=nValor;var spl=nValor.toString().split(".");var cDecimais=spl[1];var a=1/Math.pow(10,spl[1].length);var nSubsequente=nDecimais;if(nDecimais<1){return parseInt(nRetorno);}
if(cDecimais.length<=nDecimais){return parseFloat(nRetorno);}
if(parseInt(cDecimais.substr(nSubsequente,1))>5||parseInt(cDecimais.substr(nSubsequente,1))<5){nRetorno=nRetorno.toFixed(nDecimais);}else if(parseInt(cDecimais.substr(nSubsequente,1))==5){if((cDecimais.substr(nDecimais-1,1)%2)!=0){nRetorno+=a;nRetorno=nRetorno.toFixed(nDecimais);}else
if(parseInt(cDecimais.substr(parseInt(nSubsequente)+1,1))>0){nRetorno=nRetorno.toFixed(nDecimais);}else{nRetorno=truncateValue(nValor,nDecimais);}}
return parseFloat(nRetorno);}
function truncateValue(nValor,nDecimais){var nRetorno=nValor;spl=nValor.toString().split(".");var cDecimais=spl[1];if(nDecimais<1){return parseInt(nRetorno);}
if(cDecimais.length<=nDecimais){return nRetorno;}
nRetorno=parseInt(nValor.toString())+'.'+cDecimais.substr(0,nDecimais);nRetorno=parseFloat(nRetorno);return nRetorno;}
function ebfAsciiToBinary(astring){var binary="";if(astring.length>0){for(var i=0;i<astring.length;i++){var value=astring.charCodeAt(i);for(var j=7;j>=0;j--){binary+=((value>>j)&1);}}}
return binary;}
function ebfAssociateRuletoElement(tree,element,ruleName,ruleParams){tree.associateRuleToElement(element,ruleName,ruleParams);}
function ebfAssociateTabEvent(aba,rule,ruleParams){var _ruleName=rule;var _params=ruleParams;var _sys=sysCode;var _formID=idForm;$mainform().d.t.getTabByName(aba).onclick=function(){executeJSRuleNoField(_sys,_formID,_ruleName,ruleParams);}
return null;}
function ebfAssociatingComponent(component,targetComponent){var x=$c(targetComponent);var y=$c(component);x.div.appendChild(y.div);}
function ebfAsyncJavaFlowExecute(ruleName,params,ruleOk,paramsOk,ruleFail,paramsFail){var reducedName=(ruleName);var sysCode=($mainform().document.WFRForm?$mainform().document.WFRForm.sys.value:$mainform().sysCode);var formCode=($mainform().document.WFRForm?$mainform().document.WFRForm.formID.value:null);var isJava=false;try{window.eval(reducedName);}catch(ex){try{reducedName=reduceVariable(ruleName);window.eval(reducedName);}catch(ex){isJava=true;}}
var value=null;if(isJava){let url="executeRule.do?action=executeRule&pType=2&sys=";url+=sysCode+"&formID="+URLEncode(formCode,"GET")+"&ruleName="+URLEncode(ruleName,"GET");if(params&&params.length>0){if(params instanceof Array){for(i=0;i<params.length;i++){value=normalizeRuleParam(params[i]);url+="&P_"+i+"="+URLEncode(value,"GET");}}}
let xhr=new XMLHttpRequest();xhr.open("GET",url,true);xhr.onreadystatechange=function(e){if(xhr.readyState===4){if(xhr.status>=200&&this.status<=299){if(ruleOk){paramsOk=paramsOk&&paramsOk.length>0?paramsOk:new Array();if(xhr.responseText){$mainform().document._ruleReturn=null;eval(xhr.responseText);paramsOk[0]=$mainform().document._ruleReturn;}
ebfFlowExecute(ruleOk,paramsOk);}}else{if(ruleFail){paramsFail=paramsFail&&paramsFail.length>0?paramsFail:new Array();if(xhr.responseText){eval(xhr.responseText);paramsFail[0]=xhr.status;}
ebfFlowExecute(ruleFail,paramsFail);}}}};xhr.send(null);}}
function ebfAuthSMS(phone,onSuccess,onSuccessParams,onFail,onFailParams){console.log("Disponível apenas no MakerMobile");}
function ebfAuthUser(user,password,redirect,dataConnection){var url="logon.do?sys="+sysCode+"&user="+URLEncode(user)+"&password="+URLEncode(password.trim());if(dataConnection&&dataConnection!="undefined"){url+="&dataConnection="+URLEncode(dataConnection);}
IframeTransporter(url);}
function ebfBevelGetComponentValue(formBevel,bevelName,formComponent,componentName){var component=$c(bevelName,formBevel);if(component instanceof HTMLGroupBox){var iframes=component.div.getElementsByTagName("iframe");if(iframes.length>0){var iframe=iframes[0];var mainform=eval(iframe.id).mainform;var elems=mainform.controller.getAllElements();for(var i=0;i<elems.length;i++){var elem=elems[i];if(elem.id==componentName){return elem.getValue();}}}}
return null;}
function ebfBootstrapCloseModal(modal){bootstrapCloseModal(modal);}
function ebfBootstrapCreateModal(title,closeable,bodyContent,footerContent,attributes,elementAtt){return bootstrapCreateModal(title,closeable,bodyContent,footerContent,attributes,elementAtt);}
function ebfButtonNew(aba,posX,posY,width,height,description,img,id,compContainer,styleCss){var code=getCodComponent();var component=new HTMLButton(ebfGetSystemID(),ebfGetFormID(),code,posX,posY,width,height,description,img);component.id=id;component.loadComponentTime=0;component.styleCss=styleCss;var container=$mainform().d.t.getTabByName(aba);if(!container){d.t.add(aba);container=$mainform().d.t.getTabByName(aba);}
if(compContainer){component.container=compContainer;compContainer=document.getElementById(compContainer);component.design(compContainer,true);}else{component.design(container.div,true);}
document['c_'+code]=component;}
function ebfCSSImportContent(content,idCss){var lnk=document.getElementById("WFRMakerCSS");if(lnk&&idCss==null){if(lnk.styleSheet){lnk.styleSheet.cssText=content;}else{lnk.innerHTML=content+lnk.innerHTML;}}else{lnk=document.createElement('style');lnk.id=idCss?idCss:"WFRMakerCSS";lnk.setAttribute('type',"text/css");if(lnk.styleSheet){lnk.styleSheet.cssText=content;}else{lnk.innerHTML=content;}
document.body.appendChild(lnk);}}
function ebfCalendarDecMonth(comp){let rComp=$c(comp);if(rComp)
rComp.prevMonth();else
interactionError(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",comp));}
function ebfCalendarDecYear(comp){let rComp=$c(comp);if(rComp)
rComp.prevYear();else
interactionError(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",comp));}
function ebfCalendarGetMonth(comp,monthName){let rComp=$c(comp);if(rComp)
return rComp.getMonth(monthName);interactionError(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",comp));}
function ebfCalendarGetYear(comp){let rComp=$c(comp);if(rComp)
return rComp.getYear();interactionError(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",comp));}
function ebfCalendarGoToMonth(comp,month,year){let rComp=$c(comp);if(rComp){if(month&&year)
return rComp.goToMonth(month,year);return false;}
else interactionError(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",comp));}
function ebfCalendarIncMonth(comp){let rComp=$c(comp);if(rComp)
rComp.nextMonth();else
interactionError(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",comp));}
function ebfCalendarIncYear(comp){let rComp=$c(comp);if(rComp)
rComp.nextYear();else
interactionError(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",comp));}
function ebfCalendarToday(comp){let rComp=$c(comp);if(rComp)
rComp.goToday();else
interactionError(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",comp));}
function ebfCanvasCreate(bevel){var bevelComp=$c(bevel);if(bevelComp){var canvas=document.createElement("canvas");canvas.setAttribute("width",bevelComp.div.offsetWidth+"px");canvas.setAttribute("height",bevelComp.div.offsetHeight+"px");bevelComp.div.appendChild(canvas);return canvas;}}
function ebfCanvasDrawCircle(canvas,x,y,radio,fill,fillColor,line,lineColor,lineWidth){if(canvas){var ctx=canvas.getContext("2d");ctx.beginPath();ctx.arc(x,y,radio,0,2*Math.PI);if(fill){ctx.fillStyle=fillColor;ctx.fill();}
if(line){ctx.strokeStyle=lineColor;ctx.lineWidth=lineWidth;ctx.stroke();}}}
function ebfCanvasDrawEllipse(canvas,x,y,w,h,fill,fillColor,line,lineColor,lineWidth){if(canvas){var ctx=canvas.getContext("2d");var kappa=.5522848,ox=(w/2)*kappa,oy=(h/2)*kappa,xe=x+w,ye=y+h,xm=x+w/2,ym=y+h/2;ctx.beginPath();ctx.moveTo(x,ym);ctx.bezierCurveTo(x,ym-oy,xm-ox,y,xm,y);ctx.bezierCurveTo(xm+ox,y,xe,ym-oy,xe,ym);ctx.bezierCurveTo(xe,ym+oy,xm+ox,ye,xm,ye);ctx.bezierCurveTo(xm-ox,ye,x,ym+oy,x,ym);ctx.closePath();if(fill){ctx.fillStyle=fillColor;ctx.fill();}
if(line){ctx.lineWidth=lineWidth;ctx.lineColor=lineColor;ctx.stroke();}}}
function ebfCanvasDrawLine(canvas,x1,y1,x2,y2,color,lineWidth){if(canvas){var ctx=canvas.getContext('2d');ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.strokeStyle=color;ctx.lineWidth=lineWidth;ctx.stroke();}}
function ebfCanvasDrawRect(canvas,x,y,width,height,fill,fillColor,line,lineColor,lineWidth){if(canvas){var ctx=canvas.getContext("2d");if(fill){ctx.fillStyle=fillColor;}
if(line){ctx.lineWidth=lineWidth;ctx.lineColor=lineColor;}
ctx.fillRect(x,y,width,height);}}
function ebfCanvasDrawRhombus(canvas,x1,y1,d1,d2,fill,fillColor,line,lineColor,lineWidth){if(canvas){var ctx=canvas.getContext("2d");ctx.lineTo(x1+parseInt(d1/2),y1);ctx.lineTo(x1+d1,y1+parseInt(d2/2));ctx.lineTo(x1+parseInt(d1/2),y1+d2);ctx.lineTo(x1,y1+parseInt(d2/2));ctx.lineTo(x1+parseInt(d1/2),y1);if(line){ctx.lineWidth=lineWidth;ctx.lineColor=lineColor;ctx.stroke();}
if(fill){ctx.fillStyle=fillColor;ctx.fill();}}}
function ebfCanvasRemove(canvas){if(canvas){var context=canvas.getContext("2d");context.clearRect(0,0,canvas.width,canvas.height);}}
function ebfChangeComponentValueOtherForm(form,component,value){if(webrunBroadcast){const jsonProperties={};jsonProperties.formGUID=form;jsonProperties.action="wcc";jsonProperties.component=component;jsonProperties.value=value;jsonProperties.formTarget=decodeURI(mainform.formGUID);webrunBroadcast.postMessage(jsonProperties);}}
function ebfChangeCurrentFormSize(newWidth,newHeight){if(isPopup){top.resizeTo(newWidth,newHeight);}else{var floatingFormDiv=getFloatingFormDivById($mainform().idForm);floatingFormDiv.style.height=(parseInt(newHeight)+30)+"px";floatingFormDiv.style.width=parseInt(newWidth)+"px";var floatingFormIframe=floatingFormDiv.getElementsByTagName("iframe")[0];floatingFormIframe.style.height=newHeight+"px";floatingFormIframe.style.width=newWidth+"px";getFloatingFormDivById($mainform().idForm).getElementsByTagName("iframe")[0]}}
function ebfChangeCursorComponent(componentVar,typeCursor){var c=$c(componentVar);if(c){if(c.name=="HTMLLabel"){c=c.label;}else{c=c.div;}
c.style.cursor=typeCursor;}}
function ebfChangeDescription(c,d){$c(c).setDescription(d);}
function ebfChangeFormTitle(newTitle){try{if(isPopup){top.document.title=newTitle;}else{var div="WFRIframeForm"+ebfGetFormID();let parent=mainform.parent.parent.document.getElementById(div).children[0].children[0];div=parent.childElementCount>1?parent.children[1]:parent.children[0];div.innerText=newTitle;}}catch(e){console.error("Função: 'Alterar Título do Formulário' não é suportado no componente Aba ou Moldura.");return;}}
function ebfChangeImageButton(component,path){$c(component).setImage(path);}
function ebfChangeWindowStatusBar(text){if(text==null){return;}else{$mainframe().sbtext=text;}}
function ebfChannelExecuteRuleOnForm(form,ruleName,ruleParams,ruleCallback,callbackParams){if(webrunBroadcast){if(isNullable(ruleParams))ruleParams=new Array();const jsonProperties={};jsonProperties.formGUID=form;jsonProperties.action="wef";jsonProperties.flow=ruleName;jsonProperties.params=ruleParams;jsonProperties.callback=ruleCallback;jsonProperties.callbackParams=callbackParams;jsonProperties.formTarget=decodeURI(mainform.formGUID);webrunBroadcast.postMessage(jsonProperties);}}
function ebfChannelGetComponentValeuOtherForm(form,component,ruleCallback,callbackParams){if(webrunBroadcast){const jsonProperties={};jsonProperties.formGUID=form;jsonProperties.action="wgc";jsonProperties.component=component;jsonProperties.formTarget=decodeURI(mainform.formGUID);jsonProperties.callback=ruleCallback;jsonProperties.callbackParams=callbackParams;webrunBroadcast.postMessage(jsonProperties);}}
function ebfCharAt(){var retorno="";if(existArgs(arguments)){var value=arguments[0].toString();var length=value.length;var indice=parseInt(arguments[1])-1;if(indice<0){indice=0;}else if(indice>=length){indice=length-1;}
try{retorno=value.charAt(indice);}catch(ex){}}
return retorno;}
function ebfCharacter(asciiCode){var res=String.fromCharCode(asciiCode);return res;}
function ebfChatCloseActiveConversation(chat){var chatComponent=$c(chat);if(chatComponent&&chatComponent.activeContainer){chatComponent.activeContainer.setActive(false);chatComponent.activeContainer=null;}}
function ebfChatExitGroup(chat,groupId){var chatComponent=$c(chat);if(chatComponent){var chatGroup=chatComponent.getGroupById(groupId);if(chatGroup)chatGroup.groupExit();}}
function ebfChatExportConversation(chat,entityId,entityIsGroup,format,order,layout,rotated,style,borders,dateStart,dateEnd){var chatComponent=$c(chat);if(chatComponent){if(dateStart&&dateStart instanceof Date)dateStart=dateStart.toISOString();if(dateEnd&&dateEnd instanceof Date)dateEnd=dateEnd.toISOString();chatComponent.exportConversation(entityId,parseBoolean(entityIsGroup)?1:0,format,parseInt(order),parseInt(layout),parseBoolean(rotated),parseInt(style),parseBoolean(borders),dateStart,dateEnd);}}
function ebfChatGetGroupName(chat,groupId){var chatComponent=$c(chat);if(chatComponent){var chatGroup=chatComponent.getGroupById(groupId);if(chatGroup&&chatGroup.data&&chatGroup.data.name)return chatGroup.data.name;}
return"";}
function ebfChatGetGroupUsers(chat,groupId){var chatComponent=$c(chat);if(chatComponent){var chatGroup=chatComponent.getGroupById(groupId);if(chatGroup&&chatGroup.data&&chatGroup.data.users)return chatGroup.data.users;}
return[];}
function ebfChatGetTotalUnreadMessages(chat,userId){var chatComponent=$c(chat);if(chatComponent){if(userId===undefined||userId===null||userId===""){var totalUnreadMessages=0;if(chatComponent.cachedContainers&&chatComponent.cachedContainers.length>0){for(var i=0;i<chatComponent.cachedContainers.length;i++){var chatContainer=chatComponent.cachedContainers[i];if(chatContainer&&chatContainer.isUser()&&!chatContainer.isSendToEveryone&&chatContainer.unreadMessages!==undefined&&chatContainer.unreadMessages!==null){totalUnreadMessages+=chatContainer.unreadMessages;}}}
return totalUnreadMessages;}else{var chatUser=chatComponent.getUserById(userId);if(chatUser)return chatUser.unreadMessages;}}
return 0;}
function ebfChatGetUserName(chat,userId){var chatComponent=$c(chat);if(chatComponent){var chatUser=chatComponent.getUserById(userId);if(chatUser&&chatUser.data&&chatUser.data.name)return chatUser.data.name;}
return"";}
function ebfChatGroupAddUsers(chat,groupId,users){var chatComponent=$c(chat);if(chatComponent){var chatGroup=chatComponent.getGroupById(groupId);if(chatGroup)chatGroup.groupAddUsers(users);}}
function ebfChatGroupRemoveUsers(chat,groupId,users){var chatComponent=$c(chat);if(chatComponent){var chatGroup=chatComponent.getGroupById(groupId);if(chatGroup)chatGroup.groupRemoveUsers(users);}}
function ebfChatIsUserAdminOfGroup(chat,groupId,userId){var chatComponent=$c(chat);if(chatComponent){var chatGroup=chatComponent.getGroupById(groupId);if(chatGroup)return chatGroup.groupIsUserAdmin(userId);}
return false;}
function ebfChatIsUserOnline(chat,userId){var chatComponent=$c(chat);if(chatComponent){var chatUser=chatComponent.getUserById(userId);if(chatUser)return chatUser.isOnline();}
return false;}
function ebfChatOpenGroupConversation(chat,groupId){var chatComponent=$c(chat);if(chatComponent){var chatGroup=chatComponent.getGroupById(groupId);if(chatGroup)chatGroup.setActive(true);}}
function ebfChatOpenUserConversation(chat,userId){var chatComponent=$c(chat);if(chatComponent){var chatUser=chatComponent.getUserById(userId);if(chatUser)chatUser.setActive(true);}}
function ebfChatSendMessage(chat,entityId,entityIsGroup,messageContent){if(messageContent===undefined||messageContent===null||messageContent.toString().length==0||messageContent.toString().trim().length==0)return;var chatComponent=$c(chat);if(chatComponent){chatComponent.sendMessage(entityId,entityIsGroup,messageContent.toString().trim());}}
function ebfChatUpdateComponent(chat){var chatComponent=$c(chat);if(chatComponent)chatComponent.updateData(true);}
function ebfCheckBoxNew(aba,x,y,width,height,description,value,valueChecked,valueUnchecked,id,compContainer,styleCss){var code=getCodComponent();var component=new HTMLCheckbox(ebfGetSystemID(),ebfGetFormID(),code,x,y,width,height,description,value,valueChecked,valueUnchecked);if(id){component.id=id;}else{component.id=description;}
component.zindex=3;component.loadComponentTime=0;component.styleCss=styleCss;component.description=description?description:"";var container=$mainform().d.t.getTabByName(aba);if(!container){d.t.add(aba);container=$mainform().d.t.getTabByName(aba);}
if(compContainer){component.container=compContainer;compContainer=document.getElementById(compContainer);component.design(compContainer,true);}else{component.design(container.div,true);}
document['c_'+code]=component;setOrderTabDynamically(component);}
function ebfChrToAscii(achar){if(isNullable(achar)){return null;}else{return(achar.charCodeAt(0));}}
function ebfClearTimeOut(ID){if(typeof ID==='number'){window.clearTimeout(ID);}}
function ebfCloseForm(){$mainform().d.n.actExit();}
function ebfCloseFormWithoutChildren(){closeChildrenForms=false;}
function ebfCloseMasterForm(){try{if(isPopup){if($mainform().getOpenerWindow(top)){$mainform().getOpenerWindow(top).close();}
$mainform().d.n.actExit();}else{for(var i=0;i<mainSystemFrame.floatingForms.length;i++){closeFloatingFormById(mainSystemFrame.floatingForms[i].replace("WFRIframeForm",""));}}}catch(ex){}}
function ebfCloseOpenerWindow(){"use strict";var openerWindow;if(isPopup){openerWindow=$mainform().getOpenerWindow(top);if(openerWindow){openerWindow.close();openerWindow.top.close();}}else{Object.keys(mainSystemFrame.formHierarchy).forEach(function(parentFormId){var formChildren=mainSystemFrame.formHierarchy[parentFormId];formChildren.some(function(childFormId){if("WFRIframeForm"+idForm===childFormId){closeFormHierarchy(parentFormId);return true;}});});}}
function ebfComboBoxNew(aba,x,y,width,height,description,keys,values,id,compContainer,styleCss){var code=getCodComponent();var component=new HTMLComboBox(ebfGetSystemID(),ebfGetFormID(),code,x,y,width,height,description);if(!isNullable(keys)&&!isNullable(values)){if(keys instanceof Array&&values instanceof Array){component.values=values;component.keys=keys;}else{component.values=[values];component.keys=[keys];}}else{component.values=[];component.keys=[];}
component.id=id;component.zindex=3;component.loadComponentTime=0;component.styleCss=styleCss;var container=$mainform().d.t.getTabByName(aba);if(!container){d.t.add(aba);container=$mainform().d.t.getTabByName(aba);}
if(compContainer){component.container=compContainer;compContainer=document.getElementById(compContainer);component.design(compContainer,true);}else{component.design(container.div,true);}
document['c_'+code]=component;setOrderTabDynamically(component);}
function ebfComboClean(obj){obj=controller.verifyComponent(obj);if(obj&&obj.clean){obj.clean();}}
function ebfComboPut(obj,key,value){obj=controller.verifyComponent(obj);if(obj&&obj.add){obj.add(key,value);}}
function ebfComboRemoveByKey(form,obj,key){obj=controller.verifyComponent(obj);if(obj&&obj.removeByKey){obj.removeByKey(key);}}
var overwrittenEvents=new Map();overwrittenEvents.add("change","onchange");overwrittenEvents.add("blur","onblur");function ebfComponentEventAssociate(componentName,eventName,ruleName,ruleParams){var component=controller.verifyComponent(componentName);var componentDiv;if(component==null){componentDiv=$mainform().d;}else{componentDiv=component.div;}
if(typeof(ruleParams)=='undefined'||ruleParams==null){ruleParams='';}
var startsWithOn=/^on(.+)/;var found=eventName.match(startsWithOn);if(found!=null&&found!=-1){eventName=RegExp.$1;}
var associatedFunction=function(){executeJSRuleNoField(sysCode,idForm,ruleName,ruleParams);}
var event=overwrittenEvents.get(eventName);if(event!=null){component[event]=associatedFunction;}else{addEvent(componentDiv,eventName,associatedFunction,true);if(!componentDiv.ruleEvents){componentDiv.ruleEvents=new Array();}
componentDiv.ruleEvents[eventName]=associatedFunction;}
if(component){if(!component.onclick){component.onclick=function(){};}
component.setEnabled(true);}}
function ebfComponentEventRemove(componentName,eventName){var component=controller.verifyComponent(componentName);var componentDiv;if(component==null){componentDiv=$mainform().d;}else{componentDiv=component.div;}
var startsWithOn=/^on(.+)/;var found=eventName.match(startsWithOn);if(found!=null&&found!=-1){eventName=RegExp.$1;}
if(componentDiv.ruleEvents){var associatedFunction=componentDiv.ruleEvents[eventName];removeEvent(componentDiv,eventName,associatedFunction,true);componentDiv.ruleEvents[eventName]=null;}}
function ebfComponentExists(componentName){if($c(componentName))
return true;else
return false;}
function ebfComponentIsEnabled(formGUID,componentName){return $c(componentName,formGUID).getEnabled();}
function repeatValueUntilSize(s,size){var r="";for(var i=1;i<=size;i++){r+=s;}
return r;}
function convertToJsMask(m,type){var r="";if(type!="date"&&m!=null&&m.length>0){r=m;if(type=="number"){r=r.replace(/\\\\/g,"");r=r.replace(/;0/g,"");r=r.replace(/;1/g,"");r=r.replace(/\\!/g,"");r=trim(r);var li=r.lastIndexOf(".");var nm="#,###";if(m.indexOf(",")==-1){nm="#";}
if(li!=-1){nm+=".";nm+=repeatValueUntilSize("0",r.substring(li+1,r.length).length);}
r=nm;}else{r=r.replace(/\\\\0/g,"Z");r=r.replace(/\\\\9/g,"N");r=r.replace(/\\\\/g,"");r=r.replace(/\\/g,"");r=r.replace(/;0/g,"");r=r.replace(/;1/g,"");r=r.replace(/!/g,"");r=r.replace(/0/g,"#");r=r.replace(/9/g,"#");r=r.replace(/Z/g,"0");r=r.replace(/N/g,"9");r=r.replace(/A/g,"*");r=r.replace(/L/g,"x");r=trim(r);}}
return r;}
function ebfComponentSetMask(formGUID,componentName,mask,type){var component=$c(componentName,formGUID);if(component){if(isNullable(mask)){component.mask=null;return;}
if(type=='Data'){component.dateMask=mask;}else if(type=='Número'){component.numberMask=convertToJsMask(mask,"number");}else{component.textMask=convertToJsMask(mask,"string");}
if(component.maskSuport){component.designMask();component.attachEvent(component.input,'keypress',component.keypressAction);component.attachEvent(component.input,'keyup',component.keyupAction);if(component.getValue().length>0){component.mask.allowPartial=true;component.setValue(component.mask.format(component.getValue()));component.mask.allowPartial=false;}}}}
function ebfConcat(){var value="";if(existArgs(arguments)){for(var i=0;i<arguments.length;i++){if(arguments[i]==null)arguments[i]='';var temp=arguments[i].toString();value+=temp;}}
return value;}
function ebfConcatLeft(value,size,pad){if(value&&value!=null&&value.length>0)
return value.padStart(size,pad);}
function ebfConcatRight(value,size,pad){if(value&&value!==null&&value.length>0)
return value.padEnd(size,pad);}
function ebfConfirm(src){return window.confirm(src);}
function ebfConnectionType(){}
function ebfConsumeWsSsl(urlPost,postData,contentType){}
function ebfContainerNew(aba,posX,posY,width,height,description,value,styleCss){var code=getCodComponent();var component=new HTMLContainer(ebfGetSystemID(),ebfGetFormID(),code,posX,posY,width,height,description,value);component.id=value;component.loadComponentTime=0;component.styleCss=styleCss;var container=$mainform().d.t.getTabByName(aba);if(!container){d.t.add(aba);container=$mainform().d.t.getTabByName(aba);}
component.design(container.div,true);document['c_'+code]=component;}
function ebfContainerOpenForm(form,componentName,formTarget,filter,mode,scrollbars){if(typeof componentName==="string"){component=document.getElementById(componentName);}else{component=componentName;}
if(component){var scrolling=(scrollbars?"yes":"no");var url=getAbsolutContextPath();url+='form.jsp?sys='+sysCode+'&formID='+URLEncode(formTarget)+'&goto=-1&filter='+(filter?filter:'')+'&scrolling='+scrolling+'&mode='+(mode?mode:'-1');var iframe=null;var iframes=component.getElementsByTagName("iframe");if(iframes.length>0){iframe=iframes[0];var iframeTag=eval(iframe.id);if(iframeTag.formOnUnLoadAction){iframeTag.formOnUnLoadAction();}}else{var id='URLFrame'+parseInt((Math.random()*9999999));iframe=document.createElement("iframe");iframe.src=url;iframe.id=id;iframe.name=id;iframe.style.border="none";iframe.width='100%';iframe.height='100%';}
if(iframe.src!=url){iframe.src=url}
iframe.style.scrollbars=scrollbars;component.appendChild(iframe);}}
function ebfConvertJSONToVariant(obj,c){if(!c){if(obj.substring(0,12)==='JSONInstance'){obj=JSON.parse(obj.substring(13,obj.length-1));}else if(obj.substring(0,13)==='ArrayInstance'){return eval(obj.substring(14,obj.length-1));}else{return obj;}}
const mp=new Map;var objectConstructor={}.constructor;Object.keys(obj).forEach(function(k){mp.set(k,obj[k].constructor===objectConstructor?ebfConvertJSONToVariant(obj[k],true):obj[k]);});return mp;}
function ebfConvertRichText(form,componentName){var component=$c(componentName,form);if((component instanceof HTMLMemo)&&(!component.isRichText())){component.richText=2;component.richTextLoad();}}
function ebfConverterInputTextInFile(field,size){var componente=$c(field);if(componente){try{componente.input.type='file';if(size){componente.input.setAttribute("size",size);}}catch(Exception){var inputNovo=document.createElement('input');inputNovo.type='file';inputNovo.className=componente.input.className;if(size){inputNovo.setAttribute("size",size);}else{inputNovo.style.width=componente.input.style.width+"px";inputNovo.style.height=componente.input.style.height+"px";}
inputNovo.name=componente.input.name;inputNovo.id=componente.input.id;componente.context.removeChild(componente.input);componente.context.appendChild(inputNovo);componente.input=inputNovo;}}}
function ebfCreateDate(year,month,day,hour,minute,second){var date=new Date();date.setYear(year);date.setMonth(month-1);date.setDate(day);date.setHours(hour);date.setMinutes(minute);date.setSeconds(second);return date;}
function ebfCreateObjectJSON(json){try{return JSON.parse(json==null||json==""?"{}":json);}catch(ex){handleException(new Error("Texto JSON não está em um formato válido"));}}
function ebfCreateSpinner(parent,addClass){parent=parent?parent:document.body;return bootstrapCreateSpinner(parent,addClass,true)[0];}
function getCodComponent(){var components=$mainform().controller.getTabElements(parent.mainform.d.t);var max_cod=0;for(var i=0;i<components.length;i++){max_cod=Math.max(max_cod,components[i].getCode());}
var generatedCode=parseInt(''+parseInt((parseInt(9)*Math.random()))
+''+parseInt((parseInt(9)*Math.random()))
+''+parseInt((parseInt(9)*Math.random()))
+''+parseInt((parseInt(9)*Math.random()))
+''+parseInt((parseInt(9)*Math.random()))
+''+parseInt((parseInt(9)*Math.random())));return generatedCode+max_cod;}
function ebfCreateTreeView(value,tab,posx,posy,width,height){var code=getCodComponent();tree=new HTMLTreeview(sysCode,idForm,code,posx,posy,width,height,value);tree.design(mainform.d.t.getDiv(tab),true);tree.show();return tree;}
function ebfCurrentLanguage(){return resources_locale;}
function ebfDateDate(){var data=null;if(existArgs(arguments)){var temp=toDate(arguments[0]);temp.setHours(0);temp.setMinutes(0);temp.setSeconds(0);temp.setMilliseconds(0);data=temp;}
return data;}
function ebfDateDay(){var value=0;if(existArgs(arguments)){var data=toDate(arguments[0]);if(data){value=data.getDate();}}
return value;}
function ebfDateDayDifference(){var result=0;if(existArgs(arguments)){var data1=toDate(arguments[0]);var data2=toDate(arguments[1]);if(data1!=null&&data2!=null){var diff=data1.getTime()-data2.getTime();result=diff/86400000;}}
return result;}
function ebfDateHour(){var hora=-1;if(existArgs(arguments)){var data=toDate(arguments[0]);if(data){hora=data.getHours();}}
return hora;}
function ebfDateIncDay(){var data=null;if(existArgs(arguments)){data=toDate(arguments[0]);var value=arguments[1];if(data){data.incDay(value?value:0);}}
return data;}
function ebfDateIncMonth(){var data=null;if(existArgs(arguments)){data=toDate(arguments[0]);var value=arguments[1];if(data){var oldData=(new Date(data.getFullYear(),data.getMonth(),data.getDate(),data.getHours(),data.getMinutes(),data.getSeconds(),data.getMilliseconds()));data.incMonth(value?value:0);if(oldData.getDate()!=data.getDate()){data=(new Date(data.getFullYear(),data.getMonth(),0,data.getHours(),data.getMinutes(),data.getSeconds(),data.getMilliseconds()));}}}
return data;}
function ebfDateIncYear(){var data=null;if(existArgs(arguments)){data=toDate(arguments[0]);var value=arguments[1];if(data){data.incYear(value?value:0);}}
return data;}
function ebfDateMinute(){var minute=-1;if(existArgs(arguments)){var data=toDate(arguments[0]);if(data!=null){minute=data.getMinutes();}}
return minute;}
function ebfDateMonth(){var value=0;if(existArgs(arguments)){var data=toDate(arguments[0]);if(data){value=data.getMonth()+1;}}
return value;}
function ebfDateMonthDifference(){var monthDiff=0;if(existArgs(arguments)){var data1=toDate(arguments[0]);var data2=toDate(arguments[1]);if(data1!=null&&data2!=null){var yearDiff=data1.getFullYear()-data2.getFullYear();monthDiff=(yearDiff*12)+data1.getMonth()-data2.getMonth();if(data2.compareTo(data1)==-1){if(data1.getDate()<data2.getDate()){monthDiff--;}}else{if(data1.getDate()>data2.getDate()){monthDiff++;}}}}
return monthDiff;}
function ebfDateSecond(){var second=-1;if(existArgs(arguments)){var data=toDate(arguments[0]);if(data!=null){second=data.getSeconds();}}
return second;}
function ebfDateSumHour(date,value,type){if(date.getHours){var time=new Time();date=time.fromDate(date);}
switch(type){case'H':{date.incHour(value);break;}
case'M':{date.incMinute(value);break;}
case'S':{date.incSecond(value);break;}}
return date.getDate();}
function ebfDateToday(){return new Date();}
function ebfDateYear(){var value=0;if(existArgs(arguments)){var data=toDate(arguments[0]);if(data){value=data.getFullYear();}}
return value;}
function ebfDateYearDifference(){var diff=0;if(existArgs(arguments)){var data1=toDate(arguments[0]);var data2=toDate(arguments[1]);if(data1!=null&&data2!=null){diff=data1.getFullYear()-data2.getFullYear();if(data2.compareTo(data1)==-1){if(data2.getMonth()>data1.getMonth()){diff--;}else if(data2.getMonth()==data1.getMonth){if(data2.getDate()>data1.getDate()){diff--;}}}else{if(data2.getMonth()<data1.getMonth()){diff++;}else if(data2.getMonth()==data1.getMonth()){if(data2.getDate()<data1.getDate()){diff++;}}}}}
return diff;}
function ebfDeleteObject(object,attribute){return delete object[attribute];}
function ebfDelphiColorToRGB(value)
{if(value=="clNone")return"";if(value=="clAqua")return"#33FFFF";if(value=="clBlack")return"#000000";if(value=="clBlue")return"#0000FF";if(value=="clCream")return"#FFFBF0";if(value=="clFuchsia")return"#FF00FF";if(value=="clGray")return"#808080";if(value=="clGreen")return"#008000";if(value=="clLime")return"#00FF00";if(value=="clMaroon")return"#800000";if(value=="clMedGray")return"#A0A0A4";if(value=="clMoneyGreen")return"#C0DCC0";if(value=="clNavy")return"#000080";if(value=="clOlive")return"#808000";if(value=="clPurple")return"#800080";if(value=="clRed")return"#FF0000";if(value=="clSilver")return"#C0C0C0";if(value=="clSkyBlue")return"#A6CAF0";if(value=="clTeal")return"#008080";if(value=="clWhite")return"#FFFFFF";if(value=="clYellow")return"#FFFF00";value=parseInt(value);if(value<0)
{value+=33554426;}
var r="#";r+=ebfIntToHex(0x00FF&value,2);r+=ebfIntToHex(0x00FF&value>>8,2);r+=ebfIntToHex(0x00FF&value>>16,2);return r;}
function ebfDelphiStringToJavaString(delphiString){return delphiStringToJavaString(delphiString);}
function ebfDestroyComponent(componente){var c=$c(componente);if(c&&!(c instanceof HTMLMakerFlowComponent)){var cdiv=c.div;if(cdiv.parentNode){cdiv.parentNode.removeChild(cdiv);$controller().remove(c);}}else if(c){c.free();}}
function ebfDetectMobile(){var isMobile=new Array();if(navigator.userAgent.match(/Android/i)||navigator.userAgent.match(/webOS/i)||navigator.userAgent.match(/iPhone/i)||navigator.userAgent.match(/iPad/i)||navigator.userAgent.match(/iPod/i)||navigator.userAgent.match(/BlackBerry/i)||navigator.userAgent.match(/Windows Phone/i)){isMobile[0]=true;isMobile[1]=window.innerWidth;isMobile[2]=window.innerHeight;return isMobile;}else{isMobile[0]=false;isMobile[1]=window.innerWidth;isMobile[2]=window.innerHeight;return isMobile;}}
function ebfDetectScroll(elem,pos){if(pos===1)
scrollbar=elem.scrollHeight>elem.clientHeight;else if(pos===2)
scrollbar=elem.scrollWidth>elem.clientWidth;return scrollbar;}
function ebfDisableGrid(){if(existArgs(arguments)){var componentGrid=$c(arguments[0]);var disable=parseBoolean(arguments[1]);if(!componentGrid)
return handleException(new Error('Componente '+arguments[0]+' não encontrado.'));componentGrid.iscCanvas.setDisabled(disable);componentGrid.setEnabled(!disable);}
return null;}
function ebfDisconnectLocationService(){alert("Disponível apenas no Maker Mobile");}
function ebfDonwloadStart(url,showWarning){var execWin=top;if(!IE&&d&&d.n&&d.n.isModal===true){execWin=$mainframe();}
if(IE&&top.systemOnLoadAction){IframeTransporter('download?download_file='+URLEncode(url,'GET')+'&sys='+sysCode+'&formID='+URLEncode(idForm,'GET'));}else{execWin.IframeTransporter('download?download_file='+URLEncode(url,'GET')+'&sys='+sysCode+'&formID='+URLEncode(idForm,'GET'));}
if(showWarning){interactionInfo("Se o download não iniciar automaticamente clique no link abaixo: \n<a href=\""+url+"\" target=\"_NEW\">"+url+"</a>");}}
function ebfDualListClean(obj){obj=controller.verifyComponent(obj);if(obj&&obj.deleteOption){var index=0;var objSelect=obj.leftSelect;while(objSelect.options.length){obj.deleteOption(objSelect,index);}
var objSelect=obj.rightSelect;while(objSelect.options.length){obj.deleteOption(objSelect,index);}}}
function ebfDualListGetLeftSelectedValues(form,componentName){var component=$c(componentName,form);var selectedValues=new Array();var options=component.leftSelect.options;for(var i=0;i<options.length;i++){var option=options[i];if(option.selected){selectedValues.push(option.value);}}
return selectedValues;}
function ebfDualListGetRightSelectedValues(form,componentName){var component=$c(componentName,form);var selectedValues=new Array();var options=component.rightSelect.options;for(var i=0;i<options.length;i++){var option=options[i];if(option.selected){selectedValues.push(option.value);}}
return selectedValues;}
function ebfDualListPut(obj,value,label){obj=controller.verifyComponent(obj);if(obj&&obj.addItem){obj.addItem(obj.leftSelect,value,label);}}
function ebfDynamicListDefineAllFilterType(type){var initialType=3;try{initialType=parseInt(type);if(!(/[1-4]/.test(initialType))){initialType=3;}}catch(e){}
var elems=$mainform().controller.elems;for(var i=0;i<elems.length;i++){var elem=elems[i];if(elem instanceof HTMLLookup){elem.initialType=initialType;}}}
function ebfEditNew(aba,posX,posY,width,height,description,value,id,maskType,placeholder,labelPosition,autocomplete,compContainer,styleCss){var code=getCodComponent();var component=new HTMLEdit(ebfGetSystemID(),ebfGetFormID(),code,posX,posY,width,height,description,value);if(!id){id=description;}
component.id=id;component.zindex=3;component.loadComponentTime=0;component.styleCss=styleCss;if(placeholder){component.placeholder=placeholder;}
if(labelPosition){component.labelPosition=labelPosition;}
if(autocomplete){component.autocomplete=autocomplete;}
if(maskType=="data"){component.type=2;component.typeName='date';component.textMask='##/##/####';}
if(maskType=="datahora"){component.type=2;component.typeName='datetime';component.textMask='##/##/#### ##:##:##';}
if(maskType=="moeda"){component.typeName='double';component.numberMask='#,###.00';component.align='right';}
if(maskType=="inteiro"){component.typeName='integer';component.numberMask='#';component.align='right';}
var container=$mainform().d.t.getTabByName(aba);if(!container){d.t.add(aba);container=$mainform().d.t.getTabByName(aba);}
if(compContainer){component.container=compContainer;compContainer=document.getElementById(compContainer);component.design(compContainer,true);}else{component.design(container.div,true);}
document['c_'+code]=component;setOrderTabDynamically(component);}
function setOrderTabDynamically(component){if(component&&orderTab){for(i=0;i<=orderTab.length;i++){if(orderTab[i]instanceof HTMLNavigationButton||orderTab[i]instanceof HTMLNavigationButtonSingleImage){orderTab.splice(i,0,component);break;}else if(i===orderTab.length){orderTab.push(component);break;}}}}
function ebfEnableDebugMode(status){console.log('Compatível com o Maker Mobile');}
function ebfEnableDeleteButton(value){var button=d.n.btDelete;if(!button.flag){var func=button.setEnabled;button.setEnabled=function(value,exec){if(exec){button.timeout(func,0,[value]);}}
button.flag=true;}
button.setEnabled(value,true);}
function ebfEnableEditButton(enabled){var navigation=$mainform().d.n;if(navigation){navigation.canEdit=enabled;navigation.btEdit.setEnabled(enabled);}}
function ebfEnableGPS(){}
function ebfEnableGridExportData(form,comp,enable){var grid=$c(comp);if(!grid){handleException(new Error('O componente '+comp+' não encontrado.'));return false;}
if(enable){grid.contextMenu=isc.Menu.create({ID:grid.id+"mainMenu",width:150,data:[{title:getLocaleMessage("LABEL.GRID_EXPORT_DATA")},{isSeparator:true},{icon:iconPathExport+"excel.png",title:"EXCEL",click:"gridExportData('"+grid.id+"', 'XLS')"},{icon:iconPathExport+"html.png",title:"HTML",click:"gridExportData('"+grid.id+"', 'HTML')"},{icon:iconPathExport+"json.png",title:"JSON",click:"gridExportData('"+grid.id+"', 'JSON')"},{icon:iconPathExport+"list.png",title:"LISTAGEM",click:"gridExportData('"+grid.id+"', 'LST')"},{icon:iconPathExport+"pdf.png",title:"PDF",click:"gridExportData('"+grid.id+"', 'PDF')"},{icon:iconPathExport+"txt.png",title:"TEXTO",click:"gridExportData('"+grid.id+"', 'TXT')"},{icon:iconPathExport+"xml.png",title:"XML",click:"gridExportData('"+grid.id+"', 'XML')"}]});grid.iscCanvas.contextMenu=grid.contextMenu;}else{grid.iscCanvas.contextMenu=null;}
grid.iscCanvas.markForRedraw();};function ebfEnableIncludeButton(){var navigation=$mainform().d.n;if(navigation){navigation.btInclude.setEnabled(arguments[0]);}}
function ebfEndsWith(value,valueEndsWith){if(!isNullable(value))
return toString(value).endsWith(valueEndsWith);return false;}
function ebfExecuteCustomJSFunction(obj,fun,params){if(typeof(fun)==="string"){if(typeof(obj)!=="object"||obj===null)
obj=window;return obj[fun].apply(obj,params);}}
function ebfExecuteJS(js,context){return executeJS.call(this,js,context);}
function ebfExecuteJSFromWindow(newWindow,jsQuery){try{if(!newWindow){return eval(jsQuery);}else if(newWindow instanceof HTMLIFrameElement){newWindow=newWindow.contentWindow;}
return newWindow.eval(jsQuery);}catch(e){handleException(new Error(e));}}
function ebfExportFormData(formGuid,type){window.open("export.jsp?sys="+sysCode+"&formID="+URLEncode(formGuid)+"&type="+type,"ExportFormData","fullscreen");}
function ebfFacebookAppStatus(fluxo,params){var funcao=function(){window.removeEventListener("fbload",funcao,false);FB.getLoginStatus(function(response){response=[response.status];if(!isNullable(params)){for(key in params){if(params.propertyIsEnumerable(key))
response.push(params[key]);}}
ebfFlowExecute(fluxo,response);});}
if(typeof(FB)==="undefined"){window.addEventListener("fbload",funcao,false);}else{funcao();}}
function ebfFacebookComments(component,appid,colorscheme,href,num_posts,order_by){if(isNullable(appid)){throw"App ID é um parâmetro obrigatório";}
var meta=document.createElement("meta");meta.setAttribute("property","fb:app_id");meta.setAttribute("content",appid);document.head.appendChild(meta);if(typeof(FB)==="undefined"){var FBLoadEvent=document.createEvent("Event");FBLoadEvent.initEvent("fbload",false,false);window.fbAsyncInit=function(){FB.init({"appId":appid,"status":true,"xfbml":true,"version":"v2.0"});window.dispatchEvent(FBLoadEvent);};}
if(typeof(FB)==="object"){FB.init({"appId":appid,"status":true,"xfbml":true,"version":"v2.0"});}
(function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(d.getElementById(id)){return;}
js=d.createElement(s);js.id=id;js.src="//connect.facebook.net/"+$mainform().ebfCurrentLanguage()+"/sdk.js";fjs.parentNode.insertBefore(js,fjs);}(document,'script','facebook-jssdk'));var elem=$c(component).div;elem.className="fb-comments";elem.setAttribute("data-width",$c(component).getWidth());if(!isNullable(colorscheme)){elem.setAttribute("data-colorscheme",colorscheme);}
if(!isNullable(href)){elem.setAttribute("data-href",href);}
if(!isNullable(num_posts)){elem.setAttribute("data-numposts",num_posts);}
if(!isNullable(order_by)){elem.setAttribute("data-order-by",order_by);}
if(typeof(FB)!=="undefined"){FB.XFBML.parse(elem.parentNode);}}
function ebfFacebookLike(component,layout,action,show_faces,href,share){if(!window.fbAsyncInit){var FBLoadEvent=document.createEvent("Event");FBLoadEvent.initEvent("fbload",false,false);window.fbAsyncInit=function(){FB.init({"xfbml":true,"version":"v2.0"});window.dispatchEvent(FBLoadEvent);};}
(function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(d.getElementById(id)){return;}
js=d.createElement(s);js.id=id;js.src="//connect.facebook.net/"+$mainform().ebfCurrentLanguage()+"/sdk.js";fjs.parentNode.insertBefore(js,fjs);}(document,'script','facebook-jssdk'));var elem=$c(component).div;elem.className="fb-like";elem.setAttribute("data-width",$c(component).getWidth());if(!isNullable(layout)){elem.setAttribute("data-layout",layout);}
if(!isNullable(action)){elem.setAttribute("data-action",action);}
if(!isNullable(show_faces)){elem.setAttribute("data-show-faces",show_faces);}
if(!isNullable(href)){elem.setAttribute("data-href",href);}
if(!isNullable(share)){elem.setAttribute("data-share",share);}
if(typeof(FB)!=="undefined"){FB.XFBML.parse(elem.parentNode);}}
function ebfFacebookLikeBox(component,href,colorscheme,header,show_border,show_faces,stream){if(!window.fbAsyncInit){var FBLoadEvent=document.createEvent("Event");FBLoadEvent.initEvent("fbload",false,false);window.fbAsyncInit=function(){FB.init({"xfbml":true,"version":"v2.0"});window.dispatchEvent(FBLoadEvent);};}
(function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(d.getElementById(id)){return;}
js=d.createElement(s);js.id=id;js.src="//connect.facebook.net/"+$mainform().ebfCurrentLanguage()+"/sdk.js";fjs.parentNode.insertBefore(js,fjs);}(document,'script','facebook-jssdk'));var elem=$c(component).div;elem.className="fb-like-box";elem.setAttribute("data-width",$c(component).getWidth());elem.setAttribute("data-height",$c(component).getHeight());if(!isNullable(href)){elem.setAttribute("data-href",href);}
if(!isNullable(colorscheme)){elem.setAttribute("data-colorscheme",colorscheme);}
if(!isNullable(header)){elem.setAttribute("data-header",header);}
if(!isNullable(show_border)){elem.setAttribute("data-show-border",show_border);}
if(!isNullable(show_faces)){elem.setAttribute("data-show-faces",show_faces);}
if(!isNullable(stream)){elem.setAttribute("data-stream",stream);}
if(typeof(FB)!=="undefined"){FB.XFBML.parse(elem.parentNode);}}
function ebfFacebookLogin(component,appid,auto_logout_link,max_rows,onlogin,params,scope,size,show_faces){if(isNullable(appid)){throw"App ID é um parâmetro obrigatório";}
if(typeof(FB)==="undefined"){var FBLoadEvent=document.createEvent("Event");FBLoadEvent.initEvent("fbload",false,false);window.fbAsyncInit=function(){FB.init({"appId":appid,"status":true,"xfbml":true,"version":"v2.0"});window.dispatchEvent(FBLoadEvent);};}
if(typeof(FB)==="object"){FB.init({"appId":appid,"status":true,"xfbml":true,"version":"v2.0"});}
(function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(d.getElementById(id)){return;}
js=d.createElement(s);js.id=id;js.src="//connect.facebook.net/"+$mainform().ebfCurrentLanguage()+"/sdk.js";fjs.parentNode.insertBefore(js,fjs);}(document,'script','facebook-jssdk'));var elem=$c(component).div;elem.className="fb-login-button";if(!isNullable(auto_logout_link)){elem.setAttribute("data-auto-logout-link",auto_logout_link);}
if(!isNullable(max_rows)){elem.setAttribute("data-max-rows",max_rows);}
if(!isNullable(onlogin)){if(isNullable(params)){params=[];}
elem.setAttribute("data-onlogin","ebfFlowExecute('"+onlogin+"',"+(JSON.stringify(params)).replace(/\"/g,"'")+")");}
if(!isNullable(scope)){elem.setAttribute("data-scope",scope);}else{elem.setAttribute("data-scope","public_profile");}
if(!isNullable(size)){elem.setAttribute("data-size",size);}
if(!isNullable(show_faces)){elem.setAttribute("data-show-faces",show_faces);}
if(typeof(FB)!=="undefined"){FB.XFBML.parse(elem.parentNode);}}
function ebfFacebookLoginMobile(){console.log("Disponível apenas no Maker Mobile");}
function ebfFacebookPost(component,href){if(!window.fbAsyncInit){var FBLoadEvent=document.createEvent("Event");FBLoadEvent.initEvent("fbload",false,false);window.fbAsyncInit=function(){FB.init({"xfbml":true,"version":"v2.0"});window.dispatchEvent(FBLoadEvent);};}
(function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(d.getElementById(id)){return;}
js=d.createElement(s);js.id=id;js.src="//connect.facebook.net/"+$mainform().ebfCurrentLanguage()+"/sdk.js";fjs.parentNode.insertBefore(js,fjs);}(document,'script','facebook-jssdk'));var elem=$c(component).div;elem.className="fb-post";elem.setAttribute("data-width",$c(component).getWidth());if(!isNullable(href)){elem.setAttribute("data-href",href);}
if(typeof(FB)!=="undefined"){FB.XFBML.parse(elem.parentNode);}}
function ebfFacebookRecommendationsBar(appid,action,href,site,num_recommendations,side){if(isNullable(appid)){throw"App ID é um parâmetro obrigatório";}
if(typeof(FB)==="undefined"){var FBLoadEvent=document.createEvent("Event");FBLoadEvent.initEvent("fbload",false,false);window.fbAsyncInit=function(){FB.init({"appId":appid,"status":true,"xfbml":true,"version":"v2.0"});window.dispatchEvent(FBLoadEvent);};}
if(typeof(FB)==="object"){FB.init({"appId":appid,"status":true,"xfbml":true,"version":"v2.0"});}
(function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(d.getElementById(id)){return;}
js=d.createElement(s);js.id=id;js.src="//connect.facebook.net/"+$mainform().ebfCurrentLanguage()+"/sdk.js";fjs.parentNode.insertBefore(js,fjs);}(document,'script','facebook-jssdk'));var elem=document.createElement("div");elem.className="fb-recommendations-bar";document.body.appendChild(elem);if(!isNullable(action)){elem.setAttribute("data-action",action);}
if(!isNullable(href)){elem.setAttribute("data-href",href);}
if(!isNullable(site)){elem.setAttribute("data-site",site);}
if(!isNullable(num_recommendations)){elem.setAttribute("data-num-recommendations",num_recommendations);}
if(!isNullable(side)){elem.setAttribute("data-side",side);}
if(typeof(FB)!=="undefined"){FB.XFBML.parse(elem.parentNode);}}
function ebfFacebookShare(component,layout,href){if(!window.fbAsyncInit){var FBLoadEvent=document.createEvent("Event");FBLoadEvent.initEvent("fbload",false,false);window.fbAsyncInit=function(){FB.init({"xfbml":true,"version":"v2.0"});window.dispatchEvent(FBLoadEvent);};}
(function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(d.getElementById(id)){return;}
js=d.createElement(s);js.id=id;js.src="//connect.facebook.net/"+$mainform().ebfCurrentLanguage()+"/sdk.js";fjs.parentNode.insertBefore(js,fjs);}(document,'script','facebook-jssdk'));var elem=$c(component).div;elem.className="fb-share-button";elem.setAttribute("data-width",$c(component).getWidth());if(!isNullable(layout)){elem.setAttribute("data-type",layout);}
if(!isNullable(href)){elem.setAttribute("data-href",href);}
if(typeof(FB)!=="undefined"){FB.XFBML.parse(elem.parentNode);}}
function ebfFirebaseConnect(jsonConfig,url,ruleCallback,paramsRuleCallback){loadAsync("https://www.gstatic.com/firebasejs/5.2.0/firebase.js",callbackFunction);function callbackFunction(){firebase.initializeApp(jsonConfig);firebaseCallbackFunction();}
window.firebaseCallbackFunction=function(){var parametros=paramsRuleCallback;var ruleCallbackExec=ruleCallback;if(ruleCallbackExec){executeRuleFromJS(ruleCallbackExec,parametros);}}}
function loadAsync(src,callback){var script=document.createElement('script');script.src=src;script.type='text/javascript';script.async=true;if(callback!=null){if(script.readyState){script.onreadystatechange=function(){if(script.readyState=="loaded"||script.readyState=="complete"){script.onreadystatechange=null;callback();}};}else{script.onload=function(){callback();};}}
document.head.appendChild(script);}
function ebfFirebaseMonitoringData(ref,node,filter,orderType,orderData,onSuccess,onSuccessParams){var database=firebase.database().ref(node);if(filter){var first=filter.first,last=filter.last,startAt=filter.startAt,endAt=filter.endAt,equalTo=filter.equalTo;if(orderType=='F'){database=database.orderByChild(orderData);}else if(orderType=='C'){database=database.orderByKey();}else if(orderType=='V'){database=database.orderByValue();}
if(first)
database=database.limitToFirst(first);if(last)
database=database.limitToLast(last);if(filter.hasOwnProperty('startAt'))
database=database.startAt(startAt);if(filter.hasOwnProperty('endAt'))
database=database.endAt(endAt);if(filter.hasOwnProperty('equalTo'))
database=database.equalTo(equalTo);}
database.on('child_added',function(snapshot){firebaseCallbackFunction('A',snapshot.val()?snapshot.val():{},snapshot.key);});database.on('child_changed',function(snapshot){firebaseCallbackFunction('U',snapshot.val()?snapshot.val():{},snapshot.key);});database.on('child_removed',function(snapshot){firebaseCallbackFunction('D',snapshot.val()?snapshot.val():{},snapshot.key);});database.on('child_moved',function(snapshot){firebaseCallbackFunction('M',snapshot.val()?snapshot.val():{},snapshot.key);});function firebaseCallbackFunction(action,value,key){var parametros;if(onSuccessParams)parametros=[action,value,key].concat(onSuccessParams);else parametros=[action,value,key];var ruleCallback=onSuccess;if(ruleCallback){executeRuleFromJS(ruleCallback,parametros);}};}
function ebfFirebaseOnDisconnect(ref,node,data){var database=firebase.database().ref(node);database.onDisconnect().set(data);}
function ebfFirebaseReadData(ref,node,filter,orderType,orderData,onSuccess,onSuccessParams){var database=firebase.database().ref(node);if(filter){var first=filter.first,last=filter.last,startAt=filter.startAt,endAt=filter.endAt,equalTo=filter.equalTo;if(orderType=='F'){database=database.orderByChild(orderData);}else if(orderType=='C'){database=database.orderByKey();}else if(orderType=='V'){database=database.orderByValue();}
if(first)
database=database.limitToFirst(first);if(last)
database=database.limitToLast(last);if(filter.hasOwnProperty('startAt'))
database=database.startAt(startAt);if(filter.hasOwnProperty('endAt'))
database=database.endAt(endAt);if(filter.hasOwnProperty('equalTo'))
database=database.equalTo(equalTo);}
database.once('value').then(function(snapshot){return firebaseReadCallbackFunction(snapshot.val()?snapshot.val():{});});function firebaseReadCallbackFunction(value){var parametros;if(onSuccessParams)parametros=[value].concat(onSuccessParams);else parametros=[value];var ruleCallback=onSuccess;if(ruleCallback){executeRuleFromJS(ruleCallback,parametros);}};}
function ebfFirebaseWriteData(ref,node,udid,data,async,onSuccess,onSuccessParams,onError,onErrorParams){var database=firebase.database().ref(node);if(udid===''||udid==null||udid===undefined){udid=database.push().key;}
var updates={};updates[udid]=data;if(!async){database.update(updates);return udid;}else{database.update(updates).then(function(){firebaseCallbackFunction(udid,false);}).catch(function(error){firebaseCallbackFunction(error.message,true);});}
function firebaseCallbackFunction(value,error){var parametros;if(!error){if(onSuccessParams)
parametros=[value].concat(onSuccessParams);else
parametros=[value];var ruleCallback=onSuccess;if(ruleCallback){executeRuleFromJS(ruleCallback,parametros);}}else{if(onErrorParams)
parametros=[value].concat(onErrorParams);else
parametros=[value];var ruleCallbackError=onError;if(ruleCallbackError){executeRuleFromJS(ruleCallbackError,parametros);}}}}
function ebfFirstDay(month,year,formatting){var date=new Date(year,parseInt(month)-1,1);if(formatting==='undefined'||formatting==null||formatting===""){return toDate(date.getDate()+'/'+month+'/'+year);}else{return date.format(formatting)+" 00:00:00";}}
function ebfFlowExecute(ruleName,params){var reducedName=(ruleName);var sysCode=($mainform().document.WFRForm?$mainform().document.WFRForm.sys.value:$mainform().sysCode);var formCode=($mainform().document.WFRForm?$mainform().document.WFRForm.formID.value:null);var isJava=false;var ruleFunction;try{ruleFunction=window.eval(reducedName);}catch(ex){try{reducedName=reduceVariable(ruleName);ruleFunction=window.eval(reducedName);}catch(ex){isJava=true;}}
var value=null;if(isJava){if(params&&params instanceof Array&&params.length>0){value=executeSyncJavaRule(sysCode,formCode,ruleName,params);}else{value=executeSyncJavaRule(sysCode,formCode,ruleName);}}else{var ruleInstance=new ruleFunction(null,sysCode,formCode);if(ruleInstance&&ruleInstance.run){value=executeJSRule(sysCode,formCode,reducedName,params,true);}}
return value;}
function ebfFlowMultiply(ruleName,indexIni,indexEnd,increment){ruleName=trim(ruleName);var reducedName=reduceVariable(ruleName);var sysCode=($mainform().d.WFRForm?$mainform().d.WFRForm.sys.value:$mainform().sysCode);var formCode=($mainform().d.WFRForm?$mainform().d.WFRForm.formID.value:null);var isJava=false;var ruleFunction;try{ruleFunction=window.eval(reducedName);}catch(ex){isJava=true;}
var multiply=1.0;var ini=isNullable(indexIni)?1.0:parseNumeric(indexIni);var end=parseNumeric(indexEnd);var inc=1;if(parseNumeric(increment)!=0.0){inc=parseNumeric(increment);}
while(ini!=end){if(isJava){multiply*=parseNumeric(executeSyncJavaRule(sysCode,formCode,ruleName,[ini]));}else{var ruleInstance=new ruleFunction(this,sysCode,formCode);if(ruleInstance&&ruleInstance.run){multiply*=parseNumeric(ruleInstance.run(ini));}}
ini+=inc;}
if(isJava){multiply*=parseNumeric(executeSyncJavaRule(sysCode,formCode,ruleName,[ini]));}else{var ruleInstance=new ruleFunction(this,sysCode,formCode);if(ruleInstance&&ruleInstance.run){multiply*=parseNumeric(ruleInstance.run(ini));}}
return multiply;}
function ebfFlowSum(ruleName,indexIni,indexEnd,increment){ruleName=trim(ruleName);var reducedName=reduceVariable(ruleName);var sysCode=($mainform().d.WFRForm?$mainform().d.WFRForm.sys.value:$mainform().sysCode);var formCode=($mainform().d.WFRForm?$mainform().d.WFRForm.formID.value:null);var isJava=false;var ruleFunction;try{ruleFunction=window.eval(reducedName);}catch(ex){isJava=true;}
var sum=0.0;var ini=parseNumeric(indexIni);var end=parseNumeric(indexEnd);var inc=1;if(parseNumeric(increment)!=0.0){inc=parseNumeric(increment);}
while(ini!=end){if(isJava){sum+=parseNumeric(executeSyncJavaRule(sysCode,formCode,ruleName,[ini]));}else{var ruleInstance=new ruleFunction(this,sysCode,formCode);if(ruleInstance&&ruleInstance.run){sum+=parseNumeric(ruleInstance.run(ini));}}
ini+=inc;}
if(isJava){sum+=parseNumeric(executeSyncJavaRule(sysCode,formCode,ruleName,[ini]));}else{var ruleInstance=new ruleFunction(this,sysCode,formCode);if(ruleInstance&&ruleInstance.run){sum+=parseNumeric(ruleInstance.run(ini));}}
return sum;}
function ebfFormChangeComponentValue(form,com,value){try{$c(com,form).setValue(value,true);}catch(e){if((e.toString()).indexOf('NS_ERROR_FAILURE')==-1){throw(e);}else{}}}
function ebfFormChangeComponentValueAndMask(form,com,value){if(isNullable(value,true)){return null;}
try{var component=$c(com,form);if(component.mask&&component.mask.type==="number"){var mask=component.numberMask=="$"?"0.00":component.numberMask;var maskSize=mask.split(".")[1]?mask.split(".")[1].length:0;var THOUSAND_POINT=DECIMAL_POINT==","?".":",";if(parseFloat(value).formatMoney){component.setValue(parseFloat(value).formatMoney(maskSize,DECIMAL_POINT,THOUSAND_POINT),true);}else{component.setValue(value,true);if(component.mask&&component.getValue().length>0){component.mask.allowPartial=true;component.setValue(component.mask.format(component.getValue(),component));component.mask.allowPartial=false;}}}else{component.setValue(value,true);if(component.mask&&component.getValue().length>0){component.mask.allowPartial=true;component.setValue(component.mask.format(component.getValue(),component));component.mask.allowPartial=false;}}
return component.getValue();}catch(e){if(e.toString().indexOf('NS_ERROR_FAILURE')==-1){throw(e);}}
return null;}
function ebfFormCloseChildren(formGUID,reloadParent){var currentWin=window;var parentWin=getOpenerWindow(currentWin);var allWindows=new Array();allWindows.push(currentWin);while(parentWin&&parentWin!=currentWin){allWindows.push(parentWin);var tempParentWin=getOpenerWindow(parentWin);if(tempParentWin!=parentWin)
parentWin=tempParentWin;else
parentWin=null;}
var first=null;for(var i=0;i<allWindows.length;i++){if(allWindows[i].$mainform&&allWindows[i].$mainform().formGUID){if(allWindows[i].$mainform().formGUID==formGUID){if(reloadParent){first=allWindows[i];}
for(var j=i-1;j>=0;j--){try{if(allWindows[j].isPopup)
allWindows[j].top.close();else
closeFloatingFormById(allWindows[j].idForm);}catch(e){}}
break;}}}
if(first!=null){if(first.isPopup){if(IE){first.focus();first.top.location.reload(first.top.location.href);}else{first.top.location.reload();}}else{first.location.reload();}}}
function ebfFormComponentByName(){if(existArgs(arguments)){var component=controller.getElementById(arguments[0]);if(component)
return component;}
return null;}
function ebfFormCreateActiveX(nomeMoldura,id,codebase,mapa){var moldura=$c(nomeMoldura);var div=moldura.div;var actx=document.createElement("object");actx.name="activex";actx.classid="clsid:"+id;actx.codeBase=codebase;actx.width="100%";actx.height="100%";if((mapa!=null)&&(mapa instanceof Map)){var listaChaves=mapa.getKeys();for(var i=0;i<listaChaves.length;i++){var name=listaChaves[i];var value=mapa.get(listaChaves[i]);var param=document.createElement("param");param.name=name;param.value=value;actx.appendChild(param);}}
div.appendChild(actx);}
function ebfFormCreateImage(nomeMoldura,url){var moldura=controller.getElementById(nomeMoldura);var div=getDiv("imagem",0,0,moldura.getWidth(),moldura.getHeight(),1000010,true);var img=new Image(moldura.getWidth(),moldura.getHeight());div.appendChild(img);moldura.div.innerHTML='';moldura.div.appendChild(div);img.src=url;if($c(nomeMoldura).onclick){img.onclick=$c(nomeMoldura).onclick;img.style.cursor="pointer";$c(nomeMoldura).div.onclick=null;}
return div;}
function ebfFormCreateVideo(nomeMoldura,url){var moldura=$c(nomeMoldura);var div=getDiv("Video",0,0,moldura.getWidth(),moldura.getHeight(),1000010,true);var video=document.createElement("embed");video.src=url;video.frameBorder=0;video.style.left=0;video.style.top=0;video.style.width=moldura.getWidth()+"px";video.style.height=moldura.getHeight()+"px";video.setAttribute("autostart","true");div.appendChild(video);div.style.position="absolute";moldura.div.appendChild(div);return div;}
function ebfFormEditMode(){if(d.n){d.n.timeout(d.n.actEdit,100);}}
function ebfFormGetClientHeight(){return parseInt(getWindowHeight());}
function ebfFormGetComponentValue(form,com){return $c(com,form).getValue();}
function ebfFormGetHeight(){if(existArgs(arguments)){var component=$c(arguments[0]);if(component){return component.getHeight();}}}
function ebfFormGetLookupName(form,com){try{var lk=$c(com);var idx=lk.value;return lk.showValue;}catch(e){throw"Não foi possível obter o valor do componente.";}}
function ebfFormGetVisible(){var value=false;if(existArgs(arguments)){var component=$c(arguments[0]);if(component){value=component.getVisible();}}
return value;}
function ebfFormGetWidth(){if(existArgs(arguments)){var component=$c(arguments[0]);if(component){return component.getWidth();}}}
function ebfFormInsertMode(){if(d.n){d.n.timeout(d.n.actInclude,100);}}
function ebfFormIsInBrowserMode(){return(!ebfFormIsInInsertMode()&&!ebfFormIsInEditMode());}
function ebfFormIsInEditMode(){return $mainform().edit;}
function ebfFormIsInInsertMode(){return $mainform().insert;}
function ebfFormNextTab(){var tabController=$mainform().d.t;if(tabController){tabController.isCallFunction=true;tabController.openNextTab(true);tabController.isCallFunction=false;}}
function ebfFormOpenForm(formGuid){if(formGuid&&Array.isArray(formGuid)){var props={};try{for(var i=0;i<formGuid.length;i++){if(Array.isArray(formGuid[i])&&formGuid[i].length>1){props[formGuid[i][0]]=formGuid[i][1];}}}catch(e){}
eval(getContent("wfrcore?action=ruleopenform&sys="+sysCode+"&guid="+URLEncode(props.formGuid)+"&props="+URLEncode(JSON.stringify(props))));}else{eval(getContent("wfrcore?action=ruleopenform&sys="+sysCode+"&guid="+URLEncode(formGuid)));}}
function ebfFormOpenTab(tabName){var t=$mainform().d.t;t.isCallFunction=true;t.timeout(t.openTab,0,[tabName]);return t.tabsByName[tabName];}
function ebfFormPreviousTab(){var tabController=$mainform().d.t;if(tabController){tabController.isCallFunction=true;tabController.openPreviousTab(true);tabController.isCallFunction=false;}}
function ebfFormRefreshComponent(componentName){if(!isNullable(componentName)){var component=$c(componentName);component.timeout(component.refresh,0);}}
function ebfFormSetBGColor(){if(existArgs(arguments)){var component=$c(arguments[0]);if(component){component.setBGColor(arguments[1]);}}}
function ebfFormSetColor(){if(existArgs(arguments)){var component=$c(arguments[0]);if(component){component.setColor(arguments[1]);}}}
function ebfFormSetDivBGColor(comp,cor){if(comp){var component=$c(comp);if(component){component.div.style.backgroundColor=cor;}}}
function ebfFormSetEnabled(componentName,enabled){var component=$c(componentName);if(component&&!(verifyObjectType(component,"HTMLMakerFlowComponent"))){if(controller.activeElement==component){component.blur();}
component.timeout(component.setEnabled,0,[parseBoolean(enabled)]);}else if(component){component.setEnabled(enabled);}}
function ebfFormSetFocus(){if(existArgs(arguments)){var component=$c(arguments[0]);if(component){timeout(function(){component.focus();},100);}}}
function ebfFormSetHeight(){if(existArgs(arguments)){var component=$c(arguments[0]);if(component){component.setHeight(arguments[1]);}}}
function ebfFormSetLookupName(form,com,newValue){try{var lk=$c(com);lk.setShowValue(newValue);}catch(e){throw"Não foi possível Alterar o valor do lookup";}}
function ebfFormSetPosition(){var component;if(existArgs(arguments)){component=$c(arguments[0]);if(component){if(arguments[1])
component.setX(arguments[1]);if(arguments[2])
component.setY(arguments[2]);}}}
function ebfFormSetReadonly(field,readonly){var component=$c(field);if(component){component.setReadOnly(readonly);}}
function ebfFormSetRequired(){if(existArgs(arguments)){var components=arguments[0];if(components.constructor.toString().indexOf('Array')==-1)
components=[arguments[0]];for(var i=0;i<components.length;i++){var component=$c(components[i]);if(component){component.required=arguments[1];if(component.label){component.label.innerHTML=component.decorateRequired(component.description.replace(/\s/g,'&nbsp;'),component.required);}}}}}
function ebfFormSetVisible(){if(existArgs(arguments)){var component=$c(arguments[0]);if(component)
component.setVisible(parseBoolean(arguments[1]));}}
function ebfFormSetWidth(){if(existArgs(arguments)){var component=$c(arguments[0]);if(component){component.setWidth(arguments[1]);}}}
function ebfFormShowTab(){if(existArgs(arguments)){mainform.d.t.setVisible(arguments[0],arguments[1]);}}
function ebfFormZindex(){if(existArgs(arguments)){var component=$c(arguments[0]);if(component){component.div.style.zIndex=arguments[1];}}}
function ebfFormatDateTime(date,format){if(isNullable(date)||!(date instanceof Date)){return null;}
if(isNullable(format)){format="dd/MM/yyyy";}
return date.format(format);}
function ebfFormatNumber(value,mask){var money,zeroMatcher,number,beginCents,output,i,opts,decimalPrecision,signal;decimalPrecision=mask.split('.')[mask.split('.').length-1].length;value+="";if(value[0]==='-'){signal='-';value.slice(1,value.length);}else{signal='';}
if(value.indexOf('.')>0){if(value.split('.')[1].length>=1){newdPrecision=decimalPrecision-value.split('.')[1].length;for(i=0;i<newdPrecision;i++){value+='0';}}}else if(value.indexOf(',')>0){if(value.split(',')[1].length===1){value+='0';}}else{for(i=0;i<decimalPrecision;i++){value+='0';}}
opts={'precision':decimalPrecision}
opts=mergeMoneyOptions(opts);if(opts.zeroCents){opts.lastOutput=opts.lastOutput||"";zeroMatcher=("("+opts.separator+"[0]{0,"+opts.precision+"})"),zeroRegExp=new RegExp(zeroMatcher,"g"),digitsLength=value.toString().replace(/[\D]/g,"").length||0,lastDigitLength=opts.lastOutput.toString().replace(/[\D]/g,"").length||0;value=value.toString().replace(zeroRegExp,"");if(digitsLength<lastDigitLength){value=value.slice(0,value.length-1);}}
number=value.toString().replace(/[\D]/g,""),clearDelimiter=new RegExp("^(0|\\"+opts.delimiter+")"),clearSeparator=new RegExp("(\\"+opts.separator+")$"),money=number.substr(0,number.length-opts.moneyPrecision),masked=money.substr(0,money.length%3),cents=new Array(opts.precision+1).join("0");money=money.substr(money.length%3,money.length);for(i=0,len=money.length;i<len;i++){if(i%3===0){masked+=opts.delimiter;}
masked+=money[i];}
masked=masked.replace(clearDelimiter,"");masked=masked.length?masked:"0";if(!opts.zeroCents){beginCents=number.length-opts.precision,centsValue=number.substr(beginCents,opts.precision),centsLength=centsValue.length,centsSliced=(opts.precision>centsLength)?opts.precision:centsLength;cents=(cents+centsValue).slice(-centsSliced);}
output=signal+opts.unit+masked+opts.separator+cents+opts.suffixUnit;return output.replace(clearSeparator,"");};mergeMoneyOptions=function(opts){opts=opts||{};opts={precision:opts.hasOwnProperty("precision")?opts.precision:2,separator:opts.separator||",",delimiter:opts.delimiter||".",unit:opts.unit&&(opts.unit.replace(/[\s]/g,'')+" ")||"",suffixUnit:opts.suffixUnit&&(" "+opts.suffixUnit.replace(/[\s]/g,''))||"",zeroCents:opts.zeroCents,lastOutput:opts.lastOutput};opts.moneyPrecision=opts.zeroCents?0:opts.precision;return opts;}
function ebfFrameCloseForm(form,componentName){var component=$c(componentName,form);if(component instanceof HTMLGroupBox){var iframes=component.div.getElementsByTagName("iframe");if(iframes&&iframes.length>0){var iframe=iframes[0];var iframeTag=eval(iframe.id);component.div.removeChild(iframe.parentNode);}}}
function ebfFrameOpenFilteredForm(form,componentName,formTarget,scrollbars,filter,border){var component=$c(componentName,form);if(component instanceof HTMLGroupBox){var scrolling=(scrollbars?"yes":"no");var url=getAbsolutContextPath();url+='form.jsp?sys='+sysCode+'&action=openform&formID='+URLEncode(formTarget)+'&goto=-1&filter='+(filter?filter:'')+'&scrolling='+scrolling;var iframes=component.div.getElementsByTagName("iframe");if(iframes.length>0){border=(isNullable(border)?false:border);if(border){component.div.style.boxSizing="content-box";}
var iframe=iframes[0];if(iframe.src!=url){var iframeTag=eval(iframe.id);if(iframeTag.formOnUnLoadAction){iframeTag.formOnUnLoadAction();}
iframe.src=url;iframe.style.scrollbars=scrolling;}}else{ebfFrameOpenURL(form,componentName,url,scrollbars,border);}}}
function ebfFrameOpenForm(form,componentName,formTarget,scrollbars,border){ebfFrameOpenFilteredForm(form,componentName,formTarget,scrollbars,null,border);}
function ebfFrameOpenURL(formName,componentName,url,scrollbar,border){var component=controller.getElementById(componentName,formName);if(component){var id='URLFrame'+parseInt((Math.random()*9999999));var div=getDiv(id,0,0,component.getWidth(),component.getHeight(),1000010,true);var iframe=document.createElement("iframe");div.style.width="100%";iframe.frameBorder=0;iframe.setAttribute("frameborder","no");iframe.setAttribute("border",0);iframe.setAttribute("marginwidth",0);iframe.setAttribute("marginheight",0);iframe.style.left="0px";iframe.style.top="0px";iframe.style.width="100%";iframe.style.height=component.getHeight()+"px";iframe.src=url;iframe.id=id;iframe.name=id;iframe.componentName=componentName;iframe.componentForm=component.formID;div.appendChild(iframe);border=(isNullable(border)?false:border);if(border)component.div.style.boxSizing="content-box";component.div.appendChild(div);return div;}
return null;}
function ebfFrameRefreshForm(form,componentName){var component=$c(componentName,form);if(component instanceof HTMLGroupBox){var iframes=component.div.getElementsByTagName("iframe");if(iframes&&iframes.length>0){var iframe=iframes[0];var iframeTag=eval(iframe.id);if(iframeTag.formOnUnLoadAction){iframeTag.formOnUnLoadAction();}
iframeTag.location="about:blank";iframeTag.location=iframeTag.location.toString();}}}
function ebfGenerateGUID_S4(){return(((1+Math.random())*0x10000)|0).toString(16).substring(1);}
function ebfGenerateGUID(){var bloc1=ebfGenerateGUID_S4()+ebfGenerateGUID_S4();var bloc2=ebfGenerateGUID_S4();var bloc3=ebfGenerateGUID_S4();var bloc4=ebfGenerateGUID_S4();var bloc5=ebfGenerateGUID_S4()+ebfGenerateGUID_S4()+ebfGenerateGUID_S4();return(bloc1+"-"+bloc2+"-"+bloc3+"-"+bloc4+"-"+bloc5+"".toUpperCase());}
function ebfGeoFireSetPosition(){}
function ebfGeoFireStopWatching(){}
function ebfGeoFireWatchArea(){}
function ebfGetAbsolutContextPath(){return getAbsolutContextPath();}
function ebfGetActiveElement(tree){return tree.getActiveElement();}
function ebfGetActualForm(){return $mainform();}
function ebfGetBevelWindowReferenceByGuid(formGUID,com){var formRef=ebfGetWindowReferenceByGuid(formGUID);if(formRef){if(formRef.$c(com)){var iframe=formRef.$c(com).div.getElementsByTagName("iframe");if(iframe){return iframe[0].contentWindow;}
throw"Não há nenhum formulário aberto na moldura";}
throw"Formulário não encontrado";}
throw"Formulário não encontrado";}
function ebfGetBodyJSP(){return $mainform().parent.document.body;}
function ebfGetClassObject(obj){return({}).toString.call(obj).match(/\s([a-zA-Z]+)/)[1].toLowerCase()}
function ebfGetClientFormVariable(name){if(!$mainform().__storage){$mainform().__storage={};}
return $mainform().__storage[name];}
function ebfGetComponentList(form){if(form){return controller.getElementsByForm(form);}else{return controller.getAllElements();}}
function ebfGetComponentProperty(){if(existArgs(arguments)){var comp=$c(arguments[1]);if(comp){return comp[arguments[2]];}}
return null;}
function searchFormByGUIDGetComponentValueFromOtherForm(currentForm,GUID){if(currentForm&&decodeURI(currentForm.formGUID)==GUID){return currentForm;}
if(currentForm&&currentForm.mainform&&decodeURI(currentForm.mainform.formGUID)==GUID){return currentForm.mainform;}
if(currentForm.children){for(var i=0;i<currentForm.children.length;i++){try{if(currentForm.children[i].mainform){if(decodeURI(currentForm.children[i].mainform.formGUID)==GUID){return currentForm.children[i].mainform;}
var returnForm=searchFormByGUIDGetComponentValueFromOtherForm(currentForm.children[i],GUID);if(returnForm){return returnForm;}}}catch(e){}}}}
function searchFloatingFormGet(formGUID){var openFloatingForms,mainFormWindow,i,formIframe,formReference;if(isPopup){mainFormWindow=top.opener;if(mainFormWindow){while(mainFormWindow.opener){mainFormWindow=mainFormWindow.opener;}
openFloatingForms=mainFormWindow.mainSystemFrame.document.getElementsByClassName("WFRIframeForm");}}else{openFloatingForms=mainSystemFrame.document.getElementsByClassName("WFRIframeForm");}
if(openFloatingForms){for(i=0;i<openFloatingForms.length;i++){formIframe=openFloatingForms[i].getElementsByTagName("iframe")[0];if(formIframe){formReference=formIframe.contentWindow.mainform;if(formReference){if(decodeURI(formReference.formGUID)===formGUID){return formReference;}}}}}}
function searchGUIDFormComponentTabGetValueOtherForm(form){var formPrincipal;if($mainform().mainSystemFrame||top.opener){formPrincipal=$mainform().mainSystemFrame;var formFined=findGUIDFormGetValueOtherForm(formPrincipal,form);if(formFined){return formFined;}else if(top.opener&&top.opener.mainSystemFrame){formPrincipal=top.opener.mainSystemFrame;var formFined=findGUIDFormGetValueOtherForm(formPrincipal,form);if(formFined){return formFined;}}else if(mainSystemFrame.document.getElementsByTagName("iframe")){formPrincipal=mainSystemFrame.document.getElementsByTagName("iframe")[0].contentDocument.getElementsByTagName("iframe");for(i=0;i<formPrincipal.length;i++){try{var guidForm=decodeURI(formPrincipal[i].contentWindow.mainform.formGUID);if(guidForm!==undefined&&guidForm===form){return formPrincipal[i].contentWindow.mainform;}}catch(e){}}}}}
function findGUIDFormGetValueOtherForm(formP,form){if(formP){var formChildren=formP.children;if(formChildren){for(i=0;i<formChildren.length;i++){if(formChildren[i].isPopup&&formChildren[i].mainform){var guidForm=decodeURI(formChildren[i].mainform.formGUID);}else{var guidForm=decodeURI(formChildren[i].formId?formChildren[i].formId:"");}
if(guidForm===form&&formChildren[i].mainform){return formChildren[i].mainform;}}
if(formP.mainSystemFrame.document.getElementsByTagName("iframe")){var findForm=formP.mainSystemFrame.document.getElementsByTagName("iframe")[0].contentDocument.getElementsByTagName("iframe");for(i=0;i<findForm.length;i++){try{var guidForm=decodeURI(findForm[i].contentWindow.mainform.formGUID);if(guidForm!==undefined&&guidForm===form){return findForm[i].contentWindow.mainform;}}catch(e){}}}
if(formP.mainSystemFrame.document.getElementsByClassName("WFRIframeForm")){var openFloatingForms=formP.mainSystemFrame.document.getElementsByClassName("WFRIframeForm");for(i=0;i<openFloatingForms.length;i++){try{var formReference=openFloatingForms[i].children[1].children[1].contentWindow.mainform;if(decodeURI(formReference.formGUID)===form){return formReference;}}catch(e){};}}}}}
function findInMe(formGUID){var childs=parent.window.children;var form;if(childs){for(i=0;i<childs.length;i++){var guid=childs[i].mainform.formGUID;if(guid===formGUID){form=childs[i].mainform;break;}}}
return form;}
function ebfGetComponentValueFromOtherForm(formGUID,componentName){if(isNullable(formGUID)){throw'Defina um formulário para obter o valor de um componente!';}
var mainWindow=top;while(getOpenerWindow(mainWindow)!=null){var openerWindow=getOpenerWindow(mainWindow);if(openerWindow.mainform&&!isNullable(openerWindow.mainform.sysCode)){mainWindow=openerWindow;}else{break;}}
var myForm=searchFormByGUIDGetComponentValueFromOtherForm(mainWindow,formGUID);if(!myForm){myForm=searchGUIDFormComponentTabGetValueOtherForm(formGUID);}
if(!myForm){myForm=searchFloatingFormGet(formGUID);}
if(!myForm){myForm=findInMe(formGUID);}
if(myForm){var component=myForm.controller.getElementById(componentName);if(component){return component.getValue();}else{component=myForm.controller.getElementById(componentName,formGUID);if(component){return component.getValue();}else{throw'Componente não encontrado para o formulário escolhido!';}}}else{throw'O Formulário cujo componente se deseja obter não está aberto!';}}
function ebfGetComponenteXPosition(componente){var comp=controller.getElementById(componente);if(comp){return comp.getX();}}
function ebfGetComponenteYPosition(componente){var comp=controller.getElementById(componente);if(comp){return comp.getY();}}
function ebfGetCookie(name){var dc=document.cookie;var prefix=name+"=";var begin=dc.indexOf("; "+prefix);if(begin==-1){begin=dc.indexOf(prefix);if(begin!=0)
return null;}else
begin+=2;var end=document.cookie.indexOf(";",begin);if(end==-1)
end=dc.length;return unescape(dc.substring(begin+prefix.length,end));}
function ebfGetCurrentLocation(){alert("Disponível apenas no Maker Mobile");}
function ebfGetCursorX(){return $mainform().mX;}
function ebfGetCursorY(){return $mainform().mY;}
function ebfGetDualListLeftText(component){var selectIN=$c(component).leftSelect;if(selectIN){var arrElements=new Array();if(selectIN.options.length>0){for(var i=0;i<selectIN.options.length;i++){var text=selectIN.options[i].text;arrElements.push(text);}}}else
throw"O componente não é Lista Dupla";return arrElements;}
function ebfGetDualListLeftValue(component){var selectIN=$c(component).leftSelect;if(selectIN){var arrElements=new Array();if(selectIN.options.length>0){for(var i=0;i<selectIN.options.length;i++){var text=selectIN.options[i].value;arrElements.push(text);}}}else
throw"O componente não é Lista Dupla";return arrElements;}
function ebfGetDualListRightText(component){var selectIN=$c(component).rightSelect;if(selectIN){var arrElements=new Array();if(selectIN.options.length>0){for(var i=0;i<selectIN.options.length;i++){var text=selectIN.options[i].text;arrElements.push(text);}}}else
throw"O componente não é Lista Dupla";return arrElements;}
function ebfGetDualListRightValue(component){var selectIN=$c(component).rightSelect;if(selectIN){var arrElements=new Array();if(selectIN.options.length>0){for(var i=0;i<selectIN.options.length;i++){var text=selectIN.options[i].value;arrElements.push(text);}}}else
throw"O componente não é Lista Dupla";return arrElements;}
function ebfGetElementFromList(){var value=null;if(existArgs(arguments)){var position=parseInt(arguments[1])-1;position=Math.max(0,position);position=Math.min(position,(arguments[0].length-1));value=arguments[0][position];}
return value;}
function ebfGetElementFromListNoValidatePos(){var value=null;var length=arguments[0].length-1;if(existArgs(arguments)){var position=parseInt(arguments[1])-1;if(position>length){value="";}else{value=arguments[0][position];}}
return value;}
function ebfGetElementIdByReference(elementVar){if(elementVar)return elementVar.div;}
function ebfGetFloatingFormDivById(name){return $mainform().getFloatingFormDivById(name);}
function ebfGetFocusedComponent(){if(controller&&controller.activeElement)
return controller.activeElement.id;}
function searchFormByGUIDGetFormByGuid(currentForm,GUID){if(currentForm&&currentForm.formGUID==GUID){return currentForm;}
if(currentForm&&currentForm.$mainform()&&currentForm.$mainform().formGUID==GUID){return currentForm.$mainform();}
if(currentForm.children){for(var i=0;i<currentForm.children.length;i++){try{if(currentForm.children[i].$mainform()){if(currentForm.children[i].$mainform().formGUID==GUID){return currentForm.children[i].$mainform();}
var childForm=currentForm.children[i];if(currentForm.children[i].$mainform().d.n.isModal){childForm=childForm.$mainform();}
var returnForm=searchFormByGUIDGetFormByGuid(childForm,GUID);if(returnForm){return returnForm;}}}catch(e){}}}}
function ebfGetFormByGuid(formGUID){var mainWindow=top;while(getOpenerWindow(mainWindow)!=null){var openerWindow=getOpenerWindow(mainWindow);if(openerWindow.mainform&&!isNullable(openerWindow.mainform.sysCode)){mainWindow=openerWindow;}else{break;}}
return searchFormByGUIDGetFormByGuid(mainWindow,formGUID);}
function ebfGetFormID(){var formID=($mainform().d.WFRForm?$mainform().d.WFRForm.formID.value:null);return formID;}
function ebfGetFullSystemID(){return d.WFRForm.sys.value.toString();}
function ebfGetGPSCoords(flxSucess,flxError){function num(){var txt="";for(i=0;i<8;i++){txt+=new String(parseInt(parseNumeric(9)*Math.random()));}
return txt;}
var obj=new Map();obj.add('longitude',num());obj.add('latitude',num());obj.add('altitude','1000000');obj.add('accuracy','1000000');obj.add('altitude Accuracy','1000000');obj.add('heading','1000000');obj.add('speed','1000000');obj.add('timestamp','01/01/2011 12:00');var list=new Array();list.push(obj);var func=window.eval(reduceVariable(flxSucess));var system=($mainform().d.WFRForm?$mainform().d.WFRForm.sys.value:$mainform().sysCode);var sysCode=system.toString().substring(0,3);var formID=($mainform().d.WFRForm?$mainform().d.WFRForm.formID.value:null);var ruleInstance=new func(null,sysCode,formID);ruleInstance.run.apply(ruleInstance,list);}
function ebfGetGUIDActualForm(){return $mainform().formGUID;}
function ebfGetIdForm(formActual){return formActual.idForm;}
function ebfGetJSONText(object,space){return JSON.stringify(object,null,space);}
function ebfGetListKeysObjectJson(objetoJSON){if(objetoJSON){var listKeys=new Array;for(i=0;i<Object.keys(objetoJSON).length;i++){listKeys.push(Object.keys(objetoJSON)[i]);}
return listKeys;}}
function ebfGetLocalVariable(varName){return top.document[varName];}
function ebfGetNotificationStatus(){return Notification.permission;}
function ebfGetOpenerForm(formActual){return getOpenerWindow(formActual).$mainform();}
function ebfGetParentForm(formActual){return formActual.parent.parent.$mainform();}
function ebfGetRoot(tree){return tree.getRoot();}
function ebfGetRuleName(){return this.getRuleName();}
function ebfGetSelectTabStringName(){var a=ebfSelectedTab();return a.description;}
function ebfGetSessionAttribute(name,global){try{postForceUTF8;}catch(e){var isFirefoxVersionAbove3=false;var firefoxRegExp=new RegExp("firefox/(\\d+)","i");var firefoxRegExpResult=firefoxRegExp.exec(navigator.userAgent);if(firefoxRegExpResult!=null&&firefoxRegExpResult.length>1){try{var version=parseInt(firefoxRegExpResult[1]);if(version>2){isFirefoxVersionAbove3=true;}}catch(e){}}
postForceUTF8=(isFirefoxVersionAbove3||isSafari);}
var content=getContent("sessionManager.do?sys="+sysCode+"&nome="+URLEncode(name,postForceUTF8)+"&global="+global+"&acao=get");var ajaxReturn=eval(content);if(ajaxReturn){return ajaxReturn;}else{return"";}}
function ebfGetSkinFolder(){return $mainform().skin;}
function ebfGetSystemID(){var system=($mainform().d.WFRForm?$mainform().d.WFRForm.sys.value:$mainform().sysCode);return system.toString().substring(0,3);}
function ebfGetTabDivByName(tabName){var tab=$mainform().d.t.getTabByName(tabName);if(tab){return tab.div;}}
function ebfGetTabList(){var tabList=new Array();$mainform().d.t.tabs.forEach(function(element,index,array){tabList.push(element["description"])});return tabList;}
function ebfGetTimeFromDataSince70(dateVar){var date;if(dateVar==null||dateVar=='')
return null;if(dateVar instanceof Date){date=dateVar;}else{date=new Date(dateVar);}
return date.getTime();}
function ebfGetTimeSince70(){var date=new Date();return date.getTime();}
function ebfGetTypePlatform(){return"";}
function ebfGetValueObjectJson(objectJSON,key){if(objectJSON){return objectJSON[key];}else{return null;}}
function ebfGetWebrunVersion(){return VERSION;}
function ebfGetWindowReferenceByGuid(formGUID,throwException){var topLevel=isPrincipal?principal:$mainform().parent.principal;var foundWindow;if(!topLevel){topLevel=getOpenerWindow(window);while(getOpenerWindow(topLevel)!=null){topLevel=getOpenerWindow(topLevel);}
if(topLevel&&topLevel.mainform.isPrincipal)
topLevel=topLevel.mainform.principal;if(topLevel&&topLevel.$mainform().isPrincipal)
topLevel=topLevel.$mainform().principal;}
if(topLevel&&topLevel.formGUID==formGUID)
return topLevel;if(!topLevel){if(top.$mainform()&&top.$mainform().mainform&&top.$mainform().mainform.isPrincipal)
topLevel=top.$mainform().mainform.principal;}
foundWindow=ebfSearchPopupWindowRecursivelly(topLevel,formGUID);if(foundWindow){return foundWindow.$mainform();}
if(topLevel&&topLevel.$mainform().mainSystemFrame&&topLevel.$mainform().mainSystemFrame.floatingForms){for(var i=0;i<topLevel.$mainform().mainSystemFrame.floatingForms.length;i++){var currentFloatingFormWindow=topLevel.$mainform().getFloatingFormWindowById(topLevel.$mainform().mainSystemFrame.floatingForms[i].replace("WFRIframeForm",""));if(currentFloatingFormWindow.mainform.formGUID==formGUID){return currentFloatingFormWindow.mainform;}else{var found=ebfSearchPopupWindowRecursivelly(currentFloatingFormWindow.mainform,formGUID);if(found)
return found;}}}
if(throwException==undefined||throwException){throw"Formulário não encontrado";}}
function ebfSearchPopupWindowRecursivelly(window,formGUID){if(window&&window.parent&&window.parent.children){for(var i=0;i<window.parent.children.length;i++){var currentWindow=window.parent.children[i];try{var existCurrentWindow=currentWindow.$mainform();}catch(e){continue;}
if(currentWindow.$mainform()&&currentWindow.$mainform().formGUID==formGUID){return currentWindow.$mainform();}else if(currentWindow.mainform&&currentWindow.mainform.formGUID==formGUID){return currentWindow.mainform;}
var found=ebfSearchPopupWindowRecursivelly(currentWindow,formGUID);if(found)
return found;}}else if(window&&window.children){for(var i=0;i<window.children.length;i++){var currentWindow=window.children[i];try{currentWindow.$mainform();}catch(e){continue;}
if(currentWindow.$mainform()&&currentWindow.$mainform().formGUID==formGUID){return currentWindow.$mainform();}
var found=ebfSearchPopupWindowRecursivelly(currentWindow,formGUID);if(found)
return found;}}}
function ebfGridAVGColumn(form,grid,column){var sum=0;var total=0;var avg=0;var gridName=grid;var grid=$c(grid);if(!grid){handleException(new Error("Componente "+gridName+" não encontrado"));return;}
var qtdLinhas=grid.getRowCount();var ref=grid.iscCanvas;for(var i=0;i<=qtdLinhas;i++){if(i<qtdLinhas){var data=grid.isFiltered?ref.getOriginalData().localData[i]:ref.getDataSource().cacheData[i];var rNc=grid.getRealNameColumn(column);if(rNc===-1){handleException(new Error(getLocaleMessage("INFO.GRID_COLUMN_NOT_FOUND",column,grid.description===""?gridName:grid.description)));return;}
sum=parseNumeric(data[rNc]);total=total+sum;}
else
avg=total/i;}
return avg;}
function ebfGridAddColumn(grid,column){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";grid.timeout(grid.addColumn,0,[column]);}
function ebfGridAdvancedFilter(form,comp){const grid=$c(comp);if(!grid){handleException(new Error("Componente "+comp+" não encontrado"));return;}else{if(!grid.enableSimpleFilter)
grid.enableSimpleFilter=true;gridAdvancedFilter(comp);}};function ebfGridChangeScrollLeftValue(form,com,value){if(com){var grid=$c(com);if(grid.scrollLeft){grid.scrollLeft(value);}}}
function ebfGridChangeScrollTopValue(form,com,value){if(com){var grid=$c(com);if(grid.scrollTop){grid.scrollTop(value);}}}
function ebfGridCloseAllGroups(gridName){var grid=$c(gridName);if(!grid)
throw"Componente "+grid+" não encontrado";grid.closeAllGroups();}
function ebfGridCloseGroup(gridName,group){var grid=$c(gridName);if(!grid)
throw"Componente "+grid+" não encontrado";grid.closeGroup(group);}
function ebfGridColumnCode(grid,column){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";return grid.getColumnCode(column);}
function ebfGridCreateDependence(grid1,grid2,filter){$c(grid1).gridSelectRowMaster=true;$c(grid1).addDependentGrid(grid2,filter);}
function ebfGridEditableCancel(componentName){var component=$c(componentName);if(component instanceof HTMLGrid){component.timeout(component.cancel,0);}}
function ebfGridEditableDeleteRow(grid){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";if(!(grid.editing||grid.inserting)){if(!grid.editable){if(!grid.nav)grid.nav={};if(!grid.nav.btDelete)grid.nav.btDelete={};}
var edt=grid.editable;grid.editable=true;try{grid.deleteRow();}finally{grid.editable=edt;}}}
function ebfGridEditableEdit(gridName){var grid=$c(gridName);if(!grid)throw"Componente "+gridName+" não encontrado";if(grid.editable){if(!(grid.editing||grid.inserting)){if(!grid.nav)grid.nav={};if(!grid.nav.btEdit)grid.nav.btEdit={};grid.timeout(grid.edit,0);}}else{if(grid.callForm){if(!grid.enabled||grid.readOnly||!grid.parentHasData)return;var gridrn=grid.currentRow;if(gridrn>grid.data.length-1)gridrn=-2;var left=(screen.width-grid.formWidth)/2;var top=(screen.height-grid.formHeight)/2;var gt=1+parseInt(gridrn)+parseInt(grid.gridini);if(gt>0)MM_openBrWindow('form.jsp?sys='+grid.sys+'&action=openform&formID='+grid.formCode+'&align=1&mode=2&goto='+gt+'&filter=&onClose=opener.d.c_'+grid.code+'.refreshPage()',grid.formCode,'toolbar=no,location=no,status=yes,menubar=no,scrollbars=no,resizable=no,width='+grid.formWidth+',height='+grid.formHeight+',left='+left+',top='+top);}}}
function ebfGridEditableInclude(gridName){var grid=$c(gridName);if(!grid)throw"Componente "+gridName+" não encontrado";if(grid.editable){if(!grid.nav)grid.nav={};if(!grid.nav.btInclude)grid.nav.btInclude={};grid.timeout(grid.include,0);}else{if(grid.callForm){if(!grid.enabled||grid.readOnly||!grid.parentHasData)return;var gridrn=grid.currentRow;if(gridrn>grid.data.length-1)gridrn=-2;var left=(screen.width-grid.formWidth)/2;var top=(screen.height-grid.formHeight)/2;var gt=1+parseInt(gridrn)+parseInt(grid.gridini);MM_openBrWindow('form.jsp?sys='+grid.sys+'&action=openform&formID='+grid.formCode+'&align=1&mode=1&goto='+gt+'&filter=&onClose=opener.d.c_'+grid.code+'.refreshPage()',grid.formCode,'toolbar=no,location=no,status=yes,menubar=no,scrollbars=no,resizable=no,width='+grid.formWidth+',height='+grid.formHeight+',left='+left+',top='+top);}}}
function ebfGridEditablePost(grid){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";grid.post();}
function ebfGridEnableMultiSelection(comp,enable){let component=$c(comp);if(component){enable=enable?'multiple':'single';component.iscCanvas.setSelectionType(enable);}else{handleException(getLocaleMessage('ERROR.COMPONENT_FIELD_NOT_FOUND',comp));return;}}
function ebfGridEnableOrDisableGroup(grid,enable){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";return grid.enableOrDisableGroup(enable);}
function ebfGridExportData(pForm,nameGrid,format){var grade=$c(nameGrid);if(!grade){handleException(new Error(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",nameGrid)));return;}
if(format)format=format.toUpperCase();grade.exportData(format);}
function ebfGridFillFromJson(form,grid,header,values){let cGrid=$c(String(grid));if(cGrid){cGrid.setAllColumns(parseArray(header));cGrid.setAllRecords(parseArray(values));cGrid.iscCanvas.setShowFilterEditor(false);cGrid.setGridPageIni(0);cGrid.setGridPageEnd(values.length);cGrid.order=function(){};cGrid.columns=header;cGrid.iscCanvas.markForRedraw()
cGrid.noRefresh=true;}else{handleException(getLocaleMessage('ERROR.COMPONENT_FIELD_NOT_FOUND',grid));return;}}
function parseArray(object){if(!(object instanceof Array)){try{let newArray=new Array();const size=object.length;for(var i=0;i<size;i++){newArray[i]=object[i];}
return newArray;}catch(e){return object;}}
return object;}
function ebfGridFilter(grid,filter){const comp=$c(grid);if(!comp){handleException(new Error("Componente "+grid+" não encontrado"));return;}
if(comp.isFiltered)
comp.iscCanvas.clearCriteria();comp.filter(filter);comp.actRefresh=true;}
function ebfGridFindColumn(grid,column){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";try{return grid.findColumn(column);}catch(e){return-1;}}
function ebfGridFreezeColumn(pForm,nameGrid,nameColumn,freeze){var grade=$c(nameGrid);if(!grade){handleException(new Error(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",nameGrid)));return;}
if(grade.findColumn(nameColumn)==-1){handleException(new Error(getLocaleMessage("INFO.GRID_COLUMN_NOT_FOUND",nameGrid,nameColumn)));return;}
let realNameColumn=grade.getRealNameColumn(nameColumn);if(parseBoolean(freeze))grade.freezeColumn(nameColumn);else if(grade.iscCanvas.fieldIsFrozen(realNameColumn))grade.unfreezeColumn(nameColumn);}
function ebfGridGetCheckValue(grid,row,column){var check=ebfGridGetValue(grid,row,column);if(check!==null){if(check===false){return 0;}
if(check===undefined||check===""){return 2;}
if(check===true){return 1;}}}
function ebfGridGetHeaderInfo(form,comp){let grid=$c(comp);if(!grid){handleExceptiton(new Error("O componente "+comp+"não encontrado."));return;}
return grid.iscCanvas.getFields();}
function ebfGridGetNameGroups(gridName){var grid=$c(gridName);if(!grid)
throw"Componente "+grid+" não encontrado";return grid.getNameGroups();}
function ebfGridGetOffset(grid){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";return grid.gridini;}
function ebfGridGetPagingPosition(grid){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";return(Math.ceil(toDouble(grid.gridini/grid.pagingSize)))+1;}
function ebfGridGetRealNameColumn(gridName,column){var grid=$c(gridName);if(!grid)
throw"Componente "+grid+" não encontrado";return grid.getRealNameColumn(column);}
function ebfGridGetRecordsInGroup(grid,group){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";return grid.getRecordsInGroup(group);}
function ebfGridGetScrollLeftValue(form,com){if(com)
return $c(com).getHorizontalScrollPosition();return null;}
function ebfGridGetScrollTopValue(form,com){if(com)
return $c(com).getVerticalScrollPosition();return null;}
function ebfGridGetSelectedRecords(comp,onlyIndex){let component=$c(comp);if(component){if(component.iscCanvas.selectionType==='multiple'){if(!onlyIndex)return component.getSelectedRecords();else return component.getSelectedRows();}
else return new Array();}else{handleException(getLocaleMessage('ERROR.COMPONENT_FIELD_NOT_FOUND',comp));return;}}
function ebfGridGetSelectedRow(grid){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";return grid.getSelectedRow();}
function ebfGridGetSpecificGroup(gridName,group){var grid=$c(gridName);if(!grid)
throw"Componente "+grid+" não encontrado";return grid.getSpecificGroup(group);}
function ebfGridGetStatus(form,com){var grid=$c(com);if(!grid){throw"O componente passado é nulo!"}
if(!(grid instanceof HTMLGrid)){throw"O componente passado por parâmetro não é uma grade!"}
if(grid.inserting){return"inserção";}
if(grid.editing){return"edição";}
return"normal";}
function ebfGridGetValue(grid,row,column){var gridName=grid;var grid=$c(grid);if(!grid){handleException(getLocaleMessage('ERROR.COMPONENT_FIELD_NOT_FOUND',gridName));return;}
try{var ref=grid.iscCanvas;var rNc=grid.getRealNameColumn(column);var rec=null;if(grid.isGrouped())
rec=ref.groupTree.getAllItems()[row];else{if(grid.isFiltered)
rec=ref.getOriginalData().localData[row];else
rec=ref.getDataSource().cacheData[row];}
if((rec[rNc]==='&nbsp;')||(rec[rNc]===null))
return"";return rec[rNc];}catch(e){handleException(getLocaleMessage('ERROR.GRID_NO_ROW_SELECTED'));return;}}
function ebfGridGetValueInSummary(grid,column){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";return grid.getValueInSummary(column);}
function ebfGridGetValueInSummaryGroup(grid,group,column){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";return grid.getValueInSummaryGroup(group,column);}
function ebfGridGoToPagingPosition(grid,newPagePosition){var grid=$c(grid);if(newPagePosition==1){grid.paging.btFirst.children[0].click();}else{if(!grid.paging.btNext.enabled)
grid.paging.btFirst.children[0].click();grid.paging.setGoto((newPagePosition-1)*grid.pagingSize);grid.paging.btNext.children[0].click();}}
function ebfGridGroup(gridName,column){var grid=$c(gridName);if(!grid)
throw"Componente "+grid+" não encontrado";grid.group(column);}
function ebfGridInsertRow(grid){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";grid.includeNewRow();}
function ebfGridInsertRowWithoutRefresh(gridName){var grid=$c(gridName);if(!grid)throw"Componente "+gridName+" não encontrado";grid.includeNewRow(true);}
function ebfGridIsGrouped(grid){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";return grid.isGrouped();}
function ebfGridMaxColumn(form,grid,column){var valor=0;var maximo=0;var gridName=grid;var grid=$c(grid);if(!grid){handleException(new Error("Componente "+gridName+" não encontrado"));return;}
var qtdLinhas=grid.getRowCount();var ref=grid.iscCanvas;for(var i=0;i<qtdLinhas;i++){var data=ref.getRecord(i);var rNc=grid.getRealNameColumn(column);if(rNc===-1){handleException(new Error(getLocaleMessage("INFO.GRID_COLUMN_NOT_FOUND",column,grid.description===""?gridName:grid.description)));return;}
valor=parseNumeric(data[rNc]);if(valor>maximo)
maximo=valor;}
return maximo;}
function ebfGridMinColumn(form,grid,column){var valor=0;var minimo=0;var gridName=grid;var grid=$c(grid);if(!grid){handleException(new Error("Componente "+gridName+" não encontrado"));return;}
var qtdLinhas=grid.getRowCount();var ref=grid.iscCanvas;for(var i=0;i<qtdLinhas;i++){var data=ref.getRecord(i);var rNc=grid.getRealNameColumn(column);if(rNc===-1){handleException(new Error(getLocaleMessage("INFO.GRID_COLUMN_NOT_FOUND",column,grid.description===""?gridName:grid.description)));return;}
valor=parseNumeric(data[rNc]);if(i==0)
minimo=valor;else if(valor<minimo)
minimo=valor;}
return minimo;}
function ebfGridModifyColumnsWidth(formName,gridName,columnList,widthList){var grid=$c(gridName);if(!grid){handleException(new Error("Componente "+gridName+" não encontrado"));return;}
grid.setSizeColumns(columnList,widthList);}
function ebfGridOpenAllGroups(gridName){var grid=$c(gridName);if(!grid)
throw"Componente "+grid+" não encontrado";grid.openAllGroups();}
function ebfGridOpenGroup(gridName,group){var grid=$c(gridName);if(!grid)
throw"Componente "+grid+" não encontrado";grid.openGroup(group);}
function ebfGridOpenGroupConfig(grid){var gridObj=$c(grid);if(!gridObj)
throw"Componente "+grid+" não encontrado";gridObj.openGroupConfig();}
function ebfGridRefresh(grid){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";grid.actPaged=true;grid.paging.navigationAction(null,null,'first');}
function ebfGridRefreshInClient(grid){var comp=$c(grid);if(!comp){handleException(new Error("Componente "+grid+" não encontrado."));return false;}
comp.actRefresh=true;comp.refreshData();}
function ebfGridRemoveColumn(grid,column){var gridName=grid;var grid=$c(grid);if(!grid){handleException(new Error("Componente "+gridName+" não encontrado"));return;}
grid.removeColumn(column);}
function ebfGridRemoveRow(grid,row){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";grid.removeDataRow(row);}
function ebfGridRowCount(grid){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";return grid.getRowCount();}
function ebfGridSelectRow(grid,row){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";var lastRow=grid.getSelectedRow();if(lastRow>=0)
grid.clearSelectedRows(lastRow);grid.timeout(grid.selectRow,0,[parseInt(row)]);grid.timeout(grid.selectionChanged,0,[]);grid.timeout(grid.moveScrollToRow,0,[parseInt(row)]);if(row<0)
grid.currentRow=-1;}
function ebfGridSetAlignColumn(comp,nameColumn,align){let component=$c(comp);if(component){if(!component.inserting&&!component.editing){const aligns={"C":"center","D":"right","E":"left"};if(align&&aligns[align]){let idx=component.iscCanvas.getFieldNum(component.getRealNameColumn(nameColumn));if(idx>=0){component.iscCanvas.setFieldProperties(idx,{'align':aligns[align]});component.iscCanvas.markForRedraw();}else{handleException(getLocaleMessage('INFO.GRID_COLUMN_NOT_FOUND',nameColumn,comp));return;}}else{console.error("O valor informado para alinhamento não suportado");return;}}else{console.error("O componente "+comp+" não pode está em modo de inclusão/edição");return;}}else{handleException(getLocaleMessage('ERROR.COMPONENT_FIELD_NOT_FOUND',comp));return;}}
function ebfGridSetAllCheckValue(grid,column,value){var totalRows=ebfGridRowCount(grid);if(totalRows>0){var cgrid=$c(grid);var idx=cgrid.iscCanvas.showRowNumbers?(cgrid.findColumn(column)-1):cgrid.findColumn(column)
var com=cgrid.components[idx];var compCheck="componentCheck"+com;var counter=0;while(counter<totalRows){cgrid.data[counter][cgrid.getRealNameColumn(column)]=cgrid.gridCheckBox(value,cgrid[compCheck]['valueCheck'],cgrid[compCheck]['valueUnCheck'],com,counter+1,null,null);counter++}
cgrid.refreshData();}}
function ebfGridSetCellHeight(comp,height){const component=$c(comp);if(!component){handleException(getLocaleMessage('ERROR.COMPONENT_FIELD_NOT_FOUND',comp));return false;}
if(height){height=parseInt(height);if(isNaN(height)){console.error("O valor informado no segundo parâmetro não é um inteiro válido");return;}
const max_height=35;const min_height=24;if(height>max_height)height=max_height;else if(height<min_height)height=min_height;component.iscCanvas.setHeaderHeight(height);component.iscCanvas.setCellHeight(height);if(component.enableSimpleFilter)component.iscCanvas.filterEditor.setHeight(height);}}
function ebfGridSetCheckValue(grid,row,column,value){if(value==0||value==1||value==2){var cgrid=$c(grid);var idx=cgrid.iscCanvas.showRowNumbers?(cgrid.findColumn(column)-1):cgrid.findColumn(column);var com=cgrid.components[idx];var compCheck="componentCheck"+com;if(cgrid.isGrouped())row=cgrid.getRowDBCursor();cgrid.data[row][cgrid.getRealNameColumn(column)]=cgrid.gridCheckBox(value,cgrid[compCheck]['valueCheck'],cgrid[compCheck]['valueUnCheck'],com,row,null,null);cgrid.refreshData();}}
function ebfGridSetColor(form,gridName,line,color,columns){var gridObj=$c(gridName,form);if(!gridObj){handleException(new Error("Grid \""+gridName+"\" not found."));return;}
line=parseInt(line);var jCond={};jCond.color=color;jCond.row=line;if(columns!=null&&columns.length>0){jCond.colsPaint=columns;}
gridObj.conditionExpressionFlow.push(jCond);gridObj.iscCanvas.markForRedraw();}
function ebfGridSetColumn(grid,column,newColumn){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";return grid.setColumn(column,newColumn);}
function ebfGridSetFilterMode(form,comp,mode){let grid=$c(comp);if(grid){if(grid.enableSimpleFilter&&mode&&mode.length>0){mode=mode.toUpperCase();mode=mode==='INCLIENT'?0:mode==='INSERVER'?1:0;grid.filterMode=mode;}}else{handleException(new Error('Componente '+comp+' não encontrado'));return false;}}
function ebfGridSetValue(grid,row,column,value){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";grid.setCellDataByColumn(row,column,value);}
function ebfGridSetValueNoRefresh(grid,row,column,value){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";grid.data[row][grid.iscCanvas.getAllFields()[grid.findColumn(column)].name]=value;}
function ebfGridSetVisibleMainButtons(componentGrid,visible,lockEditable){var component=$c(componentGrid);if(component){if(component.editable){if(component.editing||component.inserting){component.nav.normal();}
component.nav.showNav(visible);}
component.lockEditable=Boolean(lockEditable);}else{handleException("ERRRO.COMPONENT_FIELD_NOT_FOUND",componentGrid);return false;}}
function ebfGridShowColumn(pForm,nameGrid,nameColumn,show){var grade=$c(nameGrid);if(!grade){handleException(new Error("Componente "+nameGrid+" não encontrado"));return;}
grade.setShowColumn(nameColumn,show);}
function ebfGridShowGridSummaryRow(grid,show){var grid=$c(grid);if(!grid)
throw"Componente "+grid+" não encontrado";return grid.showGridSummaryRow(show);}
function ebfGridSumColumn(form,grid,column){var sum=0;var total=0;var gridName=grid;var grid=$c(grid);if(!grid){handleException(new Error("Componente "+gridName+" não encontrado"));return;}
var qtdLinhas=grid.getRowCount();var ref=grid.iscCanvas;for(var i=0;i<qtdLinhas;i++){var data=grid.isFiltered?ref.getOriginalData().localData[i]:ref.getDataSource().cacheData[i];var rNc=grid.getRealNameColumn(column);if(rNc===-1){handleException(new Error(getLocaleMessage("INFO.GRID_COLUMN_NOT_FOUND",column,grid.description===""?gridName:grid.description)));return;}
sum=parseNumeric(data[rNc]);total=total+sum;}
return total;}
function ebfGridUngroup(gridName,column){var grid=$c(gridName);if(!grid)
throw"Componente "+grid+" não encontrado";grid.ungroup(column);}
function ebfGrigExecuteFlowOnPage(form,componentName,ruleName,ruleParams){var component=$c(componentName,form);if((component instanceof HTMLGrid)&&(component.paging)){var localRuleName=ruleName;var localRuleParams=ruleParams;component.paging.onnavigate=function(){ebfFlowExecute(localRuleName,localRuleParams);};}}
function ebfGroupBoxAddScroll(component,scrollX,scrollY){if($c(component)){var cdiv=$c(component).div;if(cdiv){cdiv.style.overflowY=ebfTrim(scrollY);cdiv.style.overflowX=ebfTrim(scrollX);}}}
function ebfGroupBoxClean(formName,componentName){var component=$c(componentName,formName);if(component instanceof HTMLGroupBox){component.div.innerHTML="";}}
function ebfGroupBoxEnabledComponents(groupBoxName,enable){var groupBox=$c(groupBoxName);if(groupBox instanceof HTMLGroupBox){var rightLimit=(groupBox.getX()+groupBox.getWidth());var bottomLimit=(groupBox.getY()+groupBox.getHeight());var elements=controller.getElementsByDiv(d.t.tabsByName[groupBox.getTabName()].div);for(var i=0;i<elements.length;i++){var element=elements[i];if(element!=groupBox){if(element.getX()>=groupBox.getX()&&element.getX()<=rightLimit){if(element.getY()>=groupBox.getY()&&element.getY()<=bottomLimit){if(isNullable(element.parentPanelCode)){element.setEnabled(enable);}}}}}
groupBox.setEnabled(enable);}}
function ebfGroupBoxGetScrollPositionLeft(component){var c=$c(component).div;return c.scrollLeft;}
function ebfGroupBoxGetScrollPositionTop(component){var c=$c(component).div;return c.scrollTop;}
function ebfGroupBoxMoveComponents(groupBoxName,posX,posY){var groupBox=$c(groupBoxName);var diffDistanceX=(posX-groupBox.getX());var diffDistanceY=(posY-groupBox.getY());if(groupBox instanceof HTMLGroupBox){var rightLimit=(groupBox.getX()+groupBox.getWidth());var bottomLimit=(groupBox.getY()+groupBox.getHeight());var elements=controller.getElementsByDiv(d.t.tabsByName[groupBox.getTabName()].div);for(var i=0;i<elements.length;i++){var element=elements[i];if(element!=groupBox){if(element.getX()>=groupBox.getX()&&element.getX()<=rightLimit){if(element.getY()>=groupBox.getY()&&element.getY()<=bottomLimit){if(isNullable(element.parentPanelCode)){element.setX(element.getX()+diffDistanceX);element.setY(element.getY()+diffDistanceY);}}}}}
groupBox.setX(posX);groupBox.setY(posY);}}
function ebfGroupBoxNew(aba,posX,posY,width,height,description,value,estilo){var code=getCodComponent();var component=new HTMLGroupBox(ebfGetSystemID(),ebfGetFormID(),code,posX,posY,width,height,description,value);component.id=value;component.style=estilo;component.zindex=1;component.loadComponentTime=0;var container=$mainform().d.t.getTabByName(aba);if(!container){d.t.add(aba);container=$mainform().d.t.getTabByName(aba);}
component.design(container.div,true);document['c_'+code]=component;}
function ebfGroupBoxRemoveComponents(groupBoxName){var groupBox=$c(groupBoxName);if(groupBox instanceof HTMLGroupBox){var rightLimit=(groupBox.getX()+groupBox.getWidth());var bottomLimit=(groupBox.getY()+groupBox.getHeight());var elements=controller.getElementsByDiv(d.t.tabsByName[groupBox.getTabName()].div);for(var i=0;i<elements.length;i++){var element=elements[i];if(element!=groupBox){if(element.getX()>=groupBox.getX()&&element.getX()<=rightLimit){if(element.getY()>=groupBox.getY()&&element.getY()<=bottomLimit){if(isNullable(element.parentPanelCode)){if(element.id){ebfDestroyComponent(element.id);}}}}}}
ebfDestroyComponent(groupBox.id);}}
function ebfGroupBoxSetPositionScrollLeft(component,position){if($c(component)){var cdiv=$c(component).div;cdiv.scrollLeft=position;}}
function ebfGroupBoxSetPositionScrollTop(component,position){if($c(component)){var cdiv=$c(component).div;cdiv.scrollTop=position;}}
function ebfGroupBoxShowComponents(groupBoxName,visible){var groupBox=$c(groupBoxName);if(groupBox instanceof HTMLGroupBox){var rightLimit=(groupBox.getX()+groupBox.getWidth());var bottomLimit=(groupBox.getY()+groupBox.getHeight());var elements=controller.getElementsByDiv(d.t.tabsByName[groupBox.getTabName()].div);for(var i=0;i<elements.length;i++){var element=elements[i];if(element!=groupBox){if(element.getX()>=groupBox.getX()&&element.getX()<=rightLimit){if(element.getY()>=groupBox.getY()&&element.getY()<=bottomLimit){if(isNullable(element.parentPanelCode)){element.setVisible(visible);}}}}}
groupBox.setVisible(visible);}}
function ebfGroupBoxZindexComponents(groupBoxName,zIndex){var groupBox=$c(groupBoxName);if(groupBox instanceof HTMLGroupBox){var rightLimit=(groupBox.getX()+groupBox.getWidth());var bottomLimit=(groupBox.getY()+groupBox.getHeight());var elements=controller.getElementsByDiv(d.t.tabsByName[groupBox.getTabName()].div);for(var i=0;i<elements.length;i++){var element=elements[i];if(element!=groupBox){if(element.getX()>=groupBox.getX()&&element.getX()<=rightLimit){if(element.getY()>=groupBox.getY()&&element.getY()<=bottomLimit){if(isNullable(element.parentPanelCode)){if(element.id){ebfFormZindex(groupBoxName,zIndex+1);}}}}}}
ebfFormZindex(groupBoxName,zIndex);}}
function ebfHTMLTableCellChangeValue(cell,value){var c=document.getElementById(cell);c.innerHTML=value;}
function ebfHTMLTableCellGetValuex(cell){var c=document.getElementById(cell);return c.innerHTML;}
function ebfHTMLTableCreate(form,componentName,width,height,bgColor,border,borderColor,cellSpace,cellPad,style,scroll){var component=$c(componentName);if(component){var div=getDiv(id,0,0,component.getWidth(),component.getHeight(),1000010,true);var id='table'+parseInt((Math.random()*9999999));var tbody=document.createElement("tbody");var table=document.createElement("table");var tableBorder;if(!(border)||(border<0)){tableBorder=0;}else{tableBorder=border;}
var tableWidth;if(!(width)||(width<=0)){tableWidth=component.getWidth();}else{tableWidth=width;}
var tableHeight;if(!(height)||(height<=0)){tableHeight=component.getHeight();}else{tableHeight=height;}
var tableCellSpace;if(!(cellSpace)||(cellSpace<0)){tableCellSpace=0;}else{tableCellSpace=cellSpace;}
var tableCellPad;if(!(cellPad)||(cellPad<0)){tableCellPad=0;}else{tableCellPad=cellPad;}
table.setAttribute("id",id);table.setAttribute("name",id);table.setAttribute("width",tableWidth+"px");table.setAttribute("height",tableHeight+"px");table.setAttribute("border",tableBorder+"px");table.setAttribute("cellpadding",tableCellSpace);table.setAttribute("cellspacing",tableCellPad);if(borderColor)
table.setAttribute("borderColor",borderColor);if(bgColor)
table.setAttribute("bgColor",bgColor);this._setStyle=function(object,styleText){if(object.style.setAttribute){object.style.setAttribute("cssText",styleText);}else{object.setAttribute("style",styleText);}}
if(style){if(style.indexOf(":")==-1){table.className=style;}else{this._setStyle(table,style);}}
table.appendChild(tbody);div.appendChild(table);if(scroll)
div.style.overflow="scroll";component.div.innerHTML="";component.div.appendChild(div);document.ebfHTMLTable=id;return id;}}
function ebfHTMLTableCreateCell(form,row,width,align,bgColor,borderColor,rowspan,colspan,text,style){if(!row){if(document.ebfHTMLTableRow){row=document.ebfHTMLTableRow;}else{return;}}
var component=$w(row);if(component){var id='td'+parseInt((Math.random()*9999999));var td=document.createElement("td");var cellWidth;if((width)&&(width<=0)){cellWidth=1;}else{cellWidth=width;}
td.setAttribute("id",id);td.setAttribute("width",cellWidth);if((align=='left')||(align=='center')||(align=='right'))
td.setAttribute("align",align);if((colspan)&&(colspan>1))
td.setAttribute("colSpan",colspan);if((rowspan)&&(rowspan>1))
td.setAttribute("rowSpan",rowspan);if(borderColor)
td.setAttribute("borderColor",borderColor);if(bgColor)
td.setAttribute("bgColor",bgColor);this._setStyle=function(object,styleText){if(object.style.setAttribute){object.style.setAttribute("cssText",styleText);}else{object.setAttribute("style",styleText);}}
if(style){if(style.indexOf(":")==-1){td.className=style;}else{this._setStyle(td,style);}}
td.innerHTML=text;component.appendChild(td);return id;}}
function ebfHTMLTableCreateRow(form,table,bgColor,borderColor,style){if(!table)
if(document.ebfHTMLTable){table=document.ebfHTMLTable;}else{return;}
var component=$w(table);if(component){var tbody=component.firstChild;var id='tr'+parseInt((Math.random()*9999999));var tr=document.createElement("tr");tr.setAttribute("id",id);if(borderColor)
tr.setAttribute("borderColor",borderColor);if(bgColor)
tr.setAttribute("bgColor",bgColor);this._setStyle=function(object,styleText){if(object.style.setAttribute){object.style.setAttribute("cssText",styleText);}else{object.setAttribute("style",styleText);}}
if(style){if(style.indexOf(":")==-1){tr.className=style;}else{this._setStyle(tr,style);}}
tbody.appendChild(tr);document.ebfHTMLTableRow=id;return id;}}
function ebfHTMLTableCreateWithArray(form,componentName,width,height,border,rowList,align,bgColor,borderColor,cellBgColor,cellSpace,cellPad,style,scroll){var component=$c(componentName);if(component){var div=getDiv(id,0,0,component.getWidth(),component.getHeight(),1000010,true);var id='table'+parseInt((Math.random()*9999999));var tbody=document.createElement("tbody");var table=document.createElement("table");var tableBorder;if(!(border)||(border<0)){tableBorder=0;}else{tableBorder=border;}
var tableWidth;if(!(width)||(width<=0)){tableWidth=component.getWidth();}else{tableWidth=width;}
var tableHeight;if(!(height)||(height<=0)){tableHeight=component.getHeight();}else{tableHeight=height;}
var tableCellSpace;if(!(cellSpace)||(cellSpace<0)){tableCellSpace=0;}else{tableCellSpace=cellSpace;}
var tableCellPad;if(!(cellPad)||(cellPad<0)){tableCellPad=0;}else{tableCellPad=cellPad;}
table.setAttribute("id",id);table.setAttribute("name",id);table.setAttribute("width",tableWidth+"px");table.setAttribute("height",tableHeight+"px");table.setAttribute("border",tableBorder+"px");table.setAttribute("cellpadding",tableCellSpace);table.setAttribute("cellspacing",tableCellPad);if(borderColor)
table.setAttribute("borderColor",borderColor);if(bgColor)
table.setAttribute("bgColor",bgColor);var idCell,idRow,tr,td,cellList,cellText;for(indexRow=0;indexRow<rowList.length;indexRow++){idRow='tr'+parseInt((Math.random()*9999999));tr=document.createElement("tr");tr.setAttribute("id",idRow);cellList=rowList[indexRow];for(indexCell=0;indexCell<cellList.length;indexCell++){idCell='td'+parseInt((Math.random()*9999999));td=document.createElement("td");td.setAttribute("id",idCell);if((align=='left')||(align=='center')||(align=='right'))
td.setAttribute("align",align);if(cellBgColor)
td.setAttribute("bgColor",cellBgColor);this._setStyle=function(object,styleText){if(object.style.setAttribute){object.style.setAttribute("cssText",styleText);}else{object.setAttribute("style",styleText);}}
if(style){if(style.indexOf(":")==-1){td.className=style;}else{this._setStyle(td,style);}}
td.innerHTML=cellList[indexCell];tr.appendChild(td);}
tbody.appendChild(tr);}
table.appendChild(tbody);div.appendChild(table);if(scroll)
div.style.overflow="scroll";component.div.innerHTML="";component.div.appendChild(div);}}
function ebfHTMLTableGetHeight(component){var c=document.getElementById(component);return c.scrollHeight;}
function ebfHTMLTableGetWidth(table){var t=document.getElementById(table);return t.scrollWidth;}
function ebfHTMLTableLineChangeValue(line,value){var l=document.getElementById(line);l.innerHTML=value;}
function ebfHiddenKeyboard(){alert('Função disponível no Maker Mobile');}
function ebfHideTree(tree){return tree.hideTree();}
function ebfHtmlAppendElementAt(element,child){if(element&&child){element.appendChild(child);}}
function ebfHtmlAppendElementAtPosition(element,child,position){position=position-1;if(element!==null&&child!==null&&position!==null&&position>=0){element.insertBefore(child,element.childNodes[position])}}
function ebfHtmlAttachFlowEvent(elementVar,eventName,flowName,ruleParams,eventObject){if(elementVar&&eventName&&flowName){if(typeof(ruleParams)=='undefined'||ruleParams==null){ruleParams=[];}
if(eventName.indexOf("on")===0){eventName=eventName.substr(2);}
var totalParams=ruleParams.length;var func=function(event){event=event||window.event;if(eventObject){if(totalParams===ruleParams.length){ruleParams.unshift(event);}else{ruleParams[0]=event;}}
var stopEvent=executeJSRuleNoField(sysCode,idForm,flowName,ruleParams);if(stopEvent===false){event.stopPropagation();event.preventDefault();}};elementVar[eventName]=func;addEvent(elementVar,eventName,func,false);}}
function ebfHtmlChildNodes(element){if(element){return element.children;}}
function ebfHtmlCloneHtmlNode(element){return element.cloneNode(true);}
function ebfHtmlCreateHtmlElement(elementVar,attributeListVar,elementAtt){if(elementVar){var element=document.createElement(elementVar);if(attributeListVar){for(var i=0;i<attributeListVar.length;i++){var currentAttribute=attributeListVar[i];element.setAttribute(currentAttribute[0],currentAttribute[1]);}}
if(elementAtt){elementAtt.appendChild(element);}
return element;}}
function ebfHtmlCssDefineStyle(element,propertyName,propertyValue){if(element&&propertyName){eval("element.style."+propertyName+" = \""+propertyValue+"\"");}}
function ebfHtmlCssGetStyle(element,propertyName,propertyValue){if(element&&propertyName){return eval("element.style."+propertyName);}}
function ebfHtmlCssRemoveStyle(element,propertyName){if(element&&propertyName){eval("element.style.removeProperty(\""+propertyName+"\")");}}
function ebfHtmlGetAttribute(element,attributeName){if(element&&attributeName){return element.getAttribute(attributeName);}}
function ebfHtmlGetBodyElement(){return $mainform().document.body;}
function ebfHtmlGetDOMAttribute(elem,attr){return elem[attr];}
function ebfHtmlGetDocumentElement(){return $mainform().document;}
function ebfHtmlGetElementByAttrName(ref,attrName){ref=ref||document;return ref.querySelectorAll('['+attrName+']')}
function ebfHtmlGetElementByClassName(classe,ref){ref=ref||document;return ref.getElementsByClassName(classe);}
function ebfHtmlGetElementById(id){try{return document.getElementById(id);}catch(e){return null;}}
function ebfHtmlGetElementsByTagName(tagName,element){element=element||document;return element.getElementsByTagName(tagName);}
function ebfHtmlGetInnerHtml(elementVar){if(elementVar){return elementVar.innerHTML;}}
function ebfHtmlGetMakerElementById(id){var component=$c(id);if(component){component=component.div;}
return component;}
function ebfHtmlGetParent(elementVar){if(elementVar)
return elementVar.parentElement;}
function ebfHtmlInnerHtml(elementVar,elementContent){if(elementVar){elementVar.innerHTML=elementContent;}}
function ebfHtmlRefreshElement(element){element.contentWindow.location.reload();}
function ebfHtmlRemoveAttribute(element,attributeName){if(element&&attributeName){element.removeAttribute(attributeName);}}
function ebfHtmlRemoveChild(element,child){if(element&&child){element.removeChild(child);}}
function ebfHtmlRemoveEvent(elementVar,eventName){if(elementVar&&eventName){if(eventName.indexOf("on")===0){eventName=eventName.substr(2);}
if(elementVar[eventName]){removeEvent(elementVar,eventName,elementVar[eventName],false);elementVar[eventName]='';}}}
function ebfHtmlSetAttribute(element,attributeName,attributeValue){if(element&&attributeName){element.setAttribute(attributeName,attributeValue);}}
function ebfHtmlSetDOMAttribute(elem,attr,value){return elem[attr]=value;}
function ebfHtmlTableToXls(tables,wsnames,wbname,appname){var uri='data:application/vnd.ms-excel;base64,',tmplWorkbookXML='<?xml version="1.0"?><?mso-application progid="Excel.Sheet"?><Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet" xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">'
+'<DocumentProperties xmlns="urn:schemas-microsoft-com:office:office"><Author>Axel Richter</Author><Created>{created}</Created></DocumentProperties>'
+'<Styles>'
+'<Style ss:ID="Currency"><NumberFormat ss:Format="Currency"></NumberFormat></Style>'
+'<Style ss:ID="Date"><NumberFormat ss:Format="Medium Date"></NumberFormat></Style>'
+'</Styles>'
+'{worksheets}</Workbook>',tmplWorksheetXML='<Worksheet ss:Name="{nameWS}"><Table>{rows}</Table></Worksheet>',tmplCellXML='<Cell{attributeStyleID}{attributeFormula}><Data ss:Type="{nameType}">{data}</Data></Cell>',base64=function(s){return window.btoa(unescape(encodeURIComponent(s)))},format=function(s,c){return s.replace(/{(\w+)}/g,function(m,p){return c[p];})}
var ctx="";var workbookXML="";var worksheetsXML="";var rowsXML="";for(var i=0;i<tables.length;i++){if(!tables[i].nodeType)tables[i]=document.getElementById(tables[i]);for(var j=0;j<tables[i].rows.length;j++){rowsXML+='<Row>'
for(var k=0;k<tables[i].rows[j].cells.length;k++){var dataType=tables[i].rows[j].cells[k].getAttribute("data-type");var dataStyle=tables[i].rows[j].cells[k].getAttribute("data-style");var dataValue=tables[i].rows[j].cells[k].getAttribute("data-value");dataValue=(dataValue)?dataValue:tables[i].rows[j].cells[k].innerHTML;var dataFormula=tables[i].rows[j].cells[k].getAttribute("data-formula");dataFormula=(dataFormula)?dataFormula:(appname=='Calc'&&dataType=='DateTime')?dataValue:null;ctx={attributeStyleID:(dataStyle=='Currency'||dataStyle=='Date')?'ss:StyleID="'+dataStyle+'"':'',nameType:(dataType=='Number'||dataType=='DateTime'||dataType=='Boolean'||dataType=='Error')?dataType:'String',data:(dataFormula)?'':dataValue,attributeFormula:(dataFormula)?' ss:Formula="'+dataFormula+'"':''};rowsXML+=format(tmplCellXML,ctx);}
rowsXML+='</Row>'}
ctx={rows:rowsXML,nameWS:wsnames[i]||'Sheet'+i};worksheetsXML+=format(tmplWorksheetXML,ctx);rowsXML="";}
ctx={created:(new Date()).getTime(),worksheets:worksheetsXML};workbookXML=format(tmplWorkbookXML,ctx);if(ie||IE||isIE||isIE11||navigator.userAgent.indexOf("Edge")!==-1){alert("Recurso indisponível no IE/Edge");}else{var link=document.createElement("a");link.download=wbname;link.href=uri+base64(workbookXML);document.body.appendChild(link);link.click();document.body.removeChild(link);}};function ebfIframeTransporter(url){IframeTransporter(url);}
function ebfImageSetURL(formGUID,componentName,url){var component=$c(componentName,formGUID);component.url=url;if(component.type==1||component.type==2||(component.getViewMode()=="stretch")){component.type=-1;component.refresh(true);component.type=3;}else{component.context.style.backgroundImage=("url("+url+")");}}
function ebfIndexOf(){var indice=0;if(existArgs(arguments)){var value=arguments[0].toString();var valueToFind=arguments[1].toString();indice=value.indexOf(valueToFind);indice=indice==-1?0:++indice;}
return indice;}
function ebfInfiniteScroll(element,ruleName,params){if(element&&ruleName){element.addEventListener('scroll',function(){if(element.scrollTop+element.clientHeight>=element.scrollHeight){ebfFlowExecute(ruleName,params);}});}}
function ebfIntToHex(value,minsize){if(!minsize)minsize=2;var i=0;var j=-1;var inp=value;value=inp;var a=parseInt(inp);var b=a.toString(16);var c=parseInt("0x"+b);if(b!='NaN')
{while(b.length<minsize)b='0'+b;return b;}}
function ebfIntegracaoGetElementById(comp,id){var component=$c(comp);if(component)return component.getElementById(id);else handleException(getLocaleMessage('ERROR.COMPONENT_FIELD_NOT_FOUND',comp));}
function ebfInvokeMethod(object,methodName,params){if(!object){throw'Objeto inválido';}
if(methodName==null||methodName==''){throw'Nome do método inválido';}
var _object=object;var _params=params;var callCmd='_object.'+methodName+'(';if(params!=null){if(params.length>0){callCmd+='_params[0]';for(index=1;index<params.length;index++){callCmd+=', _params['+index+']';}}}
callCmd+=')';return eval(callCmd);}
function ebfIsCnpj(value){if(value==null||typeof value=="undefined"||value==""){return false;}
return CNPJ(value);}
function ebfIsCpf(value){if(value==null||typeof value=="undefined"||value==""){return false;}
return CPF(value);}
function ebfIsEmail(value){if(value==null||typeof value=="undefined"||value==""){return false;}
var regExp=new RegExp(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);return regExp.test(value);}
function ebfJSONExistsKey(json,key){try{const find=Object.keys(json).find(function(e){return e===key;});if(find)return true;return false;}catch(e){}
return false;}
function ebfJSONParamsCreate(list,obj){if(list&&list instanceof Array){var objectJSON=JSON.parse('{}');for(i=0;i<list.length;i++){var key=list[i];objectJSON[key[0].toString()]=key[1];}
return obj===true?objectJSON:JSON.stringify(objectJSON);}
return null;}
function __jasperOpenReportConnectionAdd(fileURL){var altura=window.screen.availHeight,largura=window.screen.availWidth;if(isChrome){altura-=70;largura-=19;}
window.open(fileURL,fileURL,"menubar=0,toolbar=0,location=0,personalbar=0,status=0,dependent=0,scrollbars=1,resizable=1,height="+altura+",width="+largura+",screenX=0,screenY=0,fullscreen=1");}
function __jasperDownloadStart(fileURL){var invertNameFile=ebfStringReverse(fileURL);var indice=invertNameFile.indexOf("/");var nameFile=ebfStringReverse(invertNameFile.substring(0,indice));if(ie||IE||isIE||isIE11){ebfDonwloadStart(fileURL,true);}else{var link=document.createElement("a");link.download=nameFile;link.href=fileURL;document.body.appendChild(link);link.click();document.body.removeChild(link);delete link;}}
function ebfLabelNew(aba,posX,posY,width,height,value,id,index,compContainer,styleCss){var code=getCodComponent();var component=new HTMLLabel(ebfGetSystemID(),ebfGetFormID(),code,posX,posY,width,height,value);component.wrap=true;component.id=id;component.zindex=index;component.loadComponentTime=0;component.styleCss=styleCss;if($mainform().d){var container=$mainform().d.t.getTabByName(aba);if(!container){if(d){d.t.add(aba);container=$mainform().d.t.getTabByName(aba);}}
if(compContainer){component.container=compContainer;compContainer=document.getElementById(compContainer);component.design(compContainer,true);}else{component.design(container.div,true);}
document['c_'+code]=component;}}
function ebfLastDay(month,year,formatting){var date=new Date(year,month,0);formatting=(formatting==='undefined'||formatting==null||formatting==="")?'dd/MM/yyyy':formatting;return date.format(formatting)+" 23:59:59";}
function ebfLastIndexOf(){var indice=0;if(existArgs(arguments)){var value=arguments[0].toString();var valueToFind=arguments[1].toString();indice=value.lastIndexOf(valueToFind);indice=indice==-1?0:++indice;}
return indice;}
function ebfLength(){var value=0;if(existArgs(arguments)){value=arguments[0].toString().length;}
return value;}
function ebfListCreate(){return new Array();}
function ebfListExistsValue(list,value){if(list!=null&&list instanceof Array&&list.length>0)
return list.includes(value);return false;}
function ebfListImplode(list,separator){if(!(list instanceof Array)){throw"Functions ebfListImplode expects an Array.";}
var first=true;var value="";for(var i=0;i<list.length;i++){var listValue=list[i];if(first){first=false;}else if(separator!=null&&(typeof separator!="undefined")){value+=separator;}
if(listValue!=null&&(typeof listValue!="undefined")){value+=listValue;}}
return value;}
function ebfListLength(){var value=0;if(existArgs(arguments)){value=arguments[0].length;}
return value;}
function ebfListParamsCreate(){var list=new Array()
for(i=0;i<arguments.length;i++){list[i]=arguments[i];}
return list;}
function ebfListSort(lstVariant,ascending){if(lstVariant){if(ascending){return lstVariant.sort();}
return lstVariant.sort().reverse();}}
function ebfLoadScript(url,ruleCallback,paramsRuleCallback){loadAsyncWfr(url,callbackFunctionLoad);function callbackFunctionLoad(){loadCallbackFunction();}
window.loadCallbackFunction=function(){var parametros=paramsRuleCallback;var ruleCallbackExec=ruleCallback;if(ruleCallbackExec){executeRuleFromJS(ruleCallbackExec,parametros);}}}
function ebfMainFormGetInstance(){return getOpenerWindow(top).$mainform().top.$mainform();}
function ebfMapAddObject(obj,key,value){obj.add(key,value);}
function ebfMapComputeDistanceBetween(coordsOne,coordsTwo){if(coordsOne instanceof Array&&coordsTwo instanceof Array){var p1=new google.maps.LatLng(coordsOne[0],coordsOne[1]);var p2=new google.maps.LatLng(coordsTwo[0],coordsTwo[1]);return google.maps.geometry.spherical.computeDistanceBetween(p1,p2);}
return null;}
function ebfMapContainsKey(obj,key){if(obj instanceof Map){return(obj.findKey(key)!=-1);}
return false;}
function ebfMapCreateFromList(){var map=new Map();for(var i=0;i<arguments.length;i++){var params=arguments[i];if(params instanceof Array&&params.length==2){map.add(params[0],params[1]);}}
return map;}
function ebfMapCreateObject(){return new Map();}
function ebfMapGetElementAt(obj,position){if(obj instanceof Map){var keys=obj.getKeys();position=parseInt(position)-1;position=Math.max(0,position);position=Math.min(position,(keys.length-1));return keys[position];}
return null;}
function ebfMapGetObject(obj,key){return obj.get(key);}
function ebfMapKeys(obj){return obj.getKeys();}
function ebfMapLength(obj){return obj.size;}
function ebfMapRemoveObject(obj,key){if(obj instanceof Map){return obj.remove(key);}
return-1;}
function ebfMapToJson(map){var ro={};var keys=map.getKeys();for(var i=0;i<keys.length;i++){if(map.get(keys[i])instanceof Map){ro[keys[i]]=ebfMapToJson(map.get(keys[i]));}else{ro[keys[i]]=map.get(keys[i]);}};return ro;};function ebfMapValues(obj){return obj.getValues();}
function ebfMapsAddListener(map,event,flow,param,image,addmarkers){if(map){if(addmarkers==undefined){addmarkers=true;}
google.maps.event.addListener(map,event,function(e){placeMarker(e.latLng,map,image,addmarkers);});function placeMarker(position,map,image,addmarkers){if(addmarkers){var marker=new google.maps.Marker({position:position,map:map,icon:image});}
var list=new Array();var pos=position.toString();pos=pos.replace("(","");pos=pos.replace(")","");var latlgn=pos.split(",");list[0]=latlgn[0];list[1]=latlgn[1];if(param){for(i=0;i<param.length;i++){list[i+2]=param[i];}}
executeRuleFromJS(flow,list);map.panTo(position);}}}
function ebfMapsAddressFromLatLgn(lat,lgn,flow,param){var geocoder=new google.maps.Geocoder();var latlng={lat:parseFloat(lat),lng:parseFloat(lgn)};return geocoder.geocode({'location':latlng},function(results,status){var address="";if(status==google.maps.GeocoderStatus.OK){if(results[0]){address=results[0].formatted_address;}}else{console.log("Não foi possível obter o endereço a partir das coordenadas. Código do erro: "+status)}
if(param instanceof Array){param.unshift(address);}else{param=new Array();param[0]=address;}
executeRuleFromJS(flow,param);});}
function ebfMapsAngle(map,type){if(map){map.setMapTypeId(type);map.setTilt(45);}}
function ebfMapsCalcDistBtwnTwoPoints(map,addressStart,addressEnd,ModeTravel,ruleName,sucessParams,ruleNameError,errorParams){var addressPoints;var result=new Array();var service=new google.maps.DistanceMatrixService();if(map){ebfMapsTraceRoute(map,addressStart,addressEnd,addressPoints,ModeTravel);}
service.getDistanceMatrix({origins:[addressStart],destinations:[addressEnd],travelMode:ModeTravel},calc);function calc(response,status){responseElements=response.rows[0].elements[0];if(status==google.maps.DistanceMatrixStatus.OK&&responseElements.status==google.maps.DistanceMatrixElementStatus.OK){result[0]=responseElements.distance.text;result[1]=responseElements.duration.text;result[2]=responseElements.distance.value;result[3]=responseElements.duration.value;if(sucessParams instanceof Array&&sucessParams!=null){sucessParams.unshift(result);}else{sucessParams[0]=result;}
sucessParams.splice(0,0,result);executeRuleFromJS(ruleName,sucessParams);}else{if(ruleNameError!=null){executeRuleFromJS(ruleNameError,errorParams);}}}}
function ebfMapsCalcRouteCoordenate(latOrigin,lngOrigin,latDestination,lngDestination,addressPoints,travelMode,ruleName,ruleParams){var directionsService;var directionsRenderer;var addressPointsAux;var result=new Array();if(addressPoints){addressPointsAux='[';for(i=0;i<addressPoints.length;i++){if((i+1)==addressPoints.length){addressPointsAux=addressPointsAux+'{location: new google.maps.LatLng('+addressPoints[i][0]+', '+addressPoints[i][1]+')}';}else{addressPointsAux=addressPointsAux+'{location: new google.maps.LatLng('+addressPoints[i][0]+', '+addressPoints[i][1]+')}, ';}}
addressPointsAux=addressPointsAux+']';}
directionsService=new google.maps.DirectionsService();directionsRenderer=new google.maps.DirectionsRenderer();var addressStart=new google.maps.LatLng(latOrigin,lngOrigin);var addressEnd=new google.maps.LatLng(latDestination,lngDestination);var request={origin:addressStart,destination:addressEnd,waypoints:eval(addressPointsAux),optimizeWaypoints:true,travelMode:travelMode};directionsService.route(request,function(response,status){result=['','',0,0];if(status==google.maps.DirectionsStatus.OK){directionsRenderer.setDirections(response);var route=response.routes[0];result[0]=route.legs[0].distance.text;result[1]=route.legs[0].duration.text;result[2]=route.legs[0].distance.value;result[3]=route.legs[0].duration.value;}
if(ruleParams instanceof Array&&ruleParams!=null){ruleParams.unshift(result);}else{ruleParams[0]=result;}
executeRuleFromJS(ruleName,ruleParams);});return directionsRenderer;}
function ebfMapsCenterMap(map,lat,lgt){if(map){var position=new google.maps.LatLng(lat,lgt);map.setCenter(position);}}
function ebfMapsChangeIconPosition(line,symbol,perc){var icons=line.get('icons');icons[0].offset=perc+'%';line.set('icons',icons);}
function ebfMapsCodeAddress(address,flow,params,errorFlow,errorParams){var geocoder=new google.maps.Geocoder();geocoder.geocode({'address':address},function(results,status){if(status==google.maps.GeocoderStatus.OK){var gResult;gResult=results[0].geometry.location.toString().replace('(','').replace(')','');gResult=gResult.split(",");if(params instanceof Array&&params!=null){for(i=0;i<params.length;i++){gResult[i+2]=params[i];}}
executeJSRuleNoField(sysCode,idForm,flow,gResult);}else{if(errorFlow!=null){executeJSRuleNoField(sysCode,idForm,errorFlow,errorParams);}}});}
function ebfMapsCreateMarker(map,lat,lgt,title,image,animation,icon,letter,colorIcon,colorLetter,centralize,infowindow){if(map){if(icon==true&&image==null){image='https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+colorIcon.replace('#',"")+'|'+colorLetter.replace('#',"");}
var center=new google.maps.LatLng(lat,lgt);var marker=new google.maps.Marker({position:center,map:map,title:title,icon:image,animation:animation});if(centralize==true){map.setCenter(center);}
if(infowindow){var infowindow=new google.maps.InfoWindow({content:infowindow,maxWidth:400});google.maps.event.addListener(marker,'click',function(){infowindow.open(map,marker);});}
return marker;}}
function ebfMapsDrawIcon(iconSymbol,iconColor,iconOpacity,borderColor,borderWeight,iconRotation){var lineSymbol={path:eval(iconSymbol),fillColor:iconColor,fillOpacity:iconOpacity,strokeColor:borderColor,strokeWeight:borderWeight,rotation:iconRotation?iconRotation:0};return lineSymbol;}
function ebfMapsDrawRouteDinamicaly(map,latOrigin,lngOrigin,latDestination,lngDestination,travelMode,iconLine,iconPosition,iconFlex,lineColor,lineOpacity,callback,param,callbackError,paramError,addressPoints){var line;var directionsService=new google.maps.DirectionsService();var call;var callError;var addressPointsAux;if(addressPoints){addressPointsAux='[';for(i=0;i<addressPoints.length;i++){if((i+1)==addressPoints.length){addressPointsAux=addressPointsAux+'{location: new google.maps.LatLng('+addressPoints[i][0]+', '+addressPoints[i][1]+')}';}else{addressPointsAux=addressPointsAux+'{location: new google.maps.LatLng('+addressPoints[i][0]+', '+addressPoints[i][1]+')}, ';}}
addressPointsAux=addressPointsAux+']';}
if(!iconLine){iconLine={};}else{iconLine={fixedRotation:!iconFlex,icon:iconLine,offset:iconPosition+'%'}}
line=new google.maps.Polyline({strokeColor:lineColor?lineColor:'black',strokeOpacity:lineOpacity?lineOpacity:0.4,path:[],icons:[iconLine],});calcRoute();function calcRoute(){var start=new google.maps.LatLng(latOrigin,lngOrigin);var end=new google.maps.LatLng(latDestination,lngDestination);var request={origin:start,destination:end,waypoints:eval(addressPointsAux),travelMode:eval('google.maps.TravelMode.'+travelMode)};call=callback;callError=callbackError;directionsService.route(request,function(response,status){if(status==google.maps.DirectionsStatus.OK){line.duration=response.routes[0].legs[0].duration;line.distance=response.routes[0].legs[0].distance;var legs=response.routes[0].legs;for(i=0;i<legs.length;i++){var steps=legs[i].steps;for(j=0;j<steps.length;j++){var nextSegment=steps[j].path;for(k=0;k<nextSegment.length;k++){line.getPath().push(nextSegment[k]);}}}
if(call){if(param instanceof Array){param.unshift(response);}else{param=new Array();param[0]=response;}
executeRuleFromJS(call,param);}}else{if(callError){if(paramError instanceof Array){paramError.unshift(status);}else{paramError=new Array();paramError[0]=status;}
executeRuleFromJS(callError,paramError);}}});}
line.setMap(map);return line;}
function ebfMapsFrameOpenMap(form,component,zoom,lat,lgt,type,mapConfig){if(form&&component){var mapOptions={"zoom":zoom||8,"center":new google.maps.LatLng(lat,lgt),"mapTypeId":type,"gestureHandling":"greedy"};var groupBox=$c(component,form);var map=new google.maps.Map(groupBox.div,mapOptions);if(typeof MutationObserver==="function"){var mo=new MutationObserver(function(){google.maps.event.trigger(map,"resize");});mo.observe(groupBox.doc,{"attributes":true,"attributeFilter":["style"]});}
if(mapConfig!=null&&mapConfig!=''&&mapConfig!=undefined){map.setOptions(mapConfig);}
return map;}}
function ebfMapsGetCoordnateStreetView(street,flow,param){google.maps.event.addListener(street,'position_changed',function(){var position=street.getPosition();var list=new Array();var pos=position.toString();pos=pos.replace("(","");pos=pos.replace(")","");var latlgn=pos.split(",");list[0]=latlgn[0];list[1]=latlgn[1];if(param instanceof Array&&param!=null){for(i=0;i<param.length;i++){list[i+2]=param[i];}}
executeRuleFromJS(flow,list);});}
function ebfMapsGetGeoCodeFromLatLgn(lat,lgn,flow,param,resultObj){var geocoder=new google.maps.Geocoder();var latlng={lat:parseFloat(lat),lng:parseFloat(lgn)};return geocoder.geocode({'location':latlng},function(results,status){var GeoObject="";if(status==google.maps.GeocoderStatus.OK){if(resultObj){GeoObject=results;}else{if(results[0]){GeoObject=results[0].formatted_address;}}}else{console.log("Não foi possível obter o endereço a partir das coordenadas. Código do erro: "+status)}
if(param instanceof Array){param.unshift(GeoObject);}else{param=new Array();param[0]=GeoObject;}
executeRuleFromJS(flow,param);});}
function ebfMapsGetNearbySearch(map,lat,lng,radius,filter,mk,urlIcon,callback){if(isNullOrEmpty(map)){handleException(new Error("Objeto Mapa (GoogleMaps) não definido."));}else{var pyrmont=new google.maps.LatLng(lat,lng);var service;var infowindow;radius=radius===undefined||radius===null?1000:(radius*1000);var request={location:pyrmont,radius:radius,type:[filter]};infowindow=new google.maps.InfoWindow();service=new google.maps.places.PlacesService(map);service.nearbySearch(request,callBack);}
function callBack(results,status){if(status===google.maps.places.PlacesServiceStatus.OK){var lm=new Array();if(mk){for(var i=0;i<results.length;i++){lm.push(createMarkerPlace(results[i]));}}
executeRuleFromJS(callback,new Array(results,lm));}else{handleException(new Error("Houve um problema, status do erro:"+status));}};function createMarkerPlace(place){var placeLoc=place.geometry.location;urlIcon=urlIcon===undefined||urlIcon===null?place.icon:urlIcon;var image={url:urlIcon,size:new google.maps.Size(20,20),scaledSize:new google.maps.Size(20,20)};var options={map:map,position:placeLoc,icon:image};var marker=new google.maps.Marker(options);google.maps.event.addListener(marker,'click',function(){infowindow.setContent(place.name);infowindow.open(map,this);});return marker;};};function ebfMapsImportLibrary(key,callbackRule,Params){window.googlemapsCallbackFunction=function(){var parametros=Params;var ruleCallback=callbackRule;if(ruleCallback){executeRuleFromJS(callbackRule,parametros);}}
var library=document.createElement("script");var url="//maps.googleapis.com/maps/api/js?sensor=false&callback=googlemapsCallbackFunction&libraries=geometry,places";if(key){url=url+"&key="+key;}
library.setAttribute("type","text/javascript");library.setAttribute("src",url);document.head.appendChild(library);}
function ebfMapsPolygonsArea(map,lat,color,borderOpacity,borderWeight,areaOpacity){var lats=[];for(var i=0;i<lat.length;i++){var aux=lat[i]
var mapAux=new Object();mapAux['lat']=aux[0];mapAux['lng']=aux[1]
lats.push(mapAux);}
var poly=new google.maps.Polygon({map:map,paths:lats,strokeColor:color,strokeOpacity:borderOpacity,strokeWeight:borderWeight,fillColor:color,fillOpacity:areaOpacity,draggable:false});poly.setMap(map);return poly;}
function ebfMapsRemoveAllListeners(map){if(map){google.maps.event.clearInstanceListeners(map);}}
function ebfMapsRemoveMarkers(marker){if(marker){if(marker instanceof Array){for(i=0;i<marker.length;i++){if(marker[i]instanceof google.maps.Marker){marker[i].setMap(null);}}}
if(marker instanceof google.maps.Marker){marker.setMap(null);}}}
function ebfMapsSetOverlay(map,mapLayer,opt,visible){if(mapLayer instanceof google.maps.MVCObject&&typeof mapLayer.setMap==='function'){mapLayer.setMap(null);}
if(opt===1||opt==='1'){mapLayer=new google.maps.TrafficLayer();}else if(opt===2||opt==='2'){mapLayer=new google.maps.TransitLayer();}else if(opt===3||opt==='3'){mapLayer=new google.maps.BicyclingLayer();}
if(visible){mapLayer.setMap(map);}else{mapLayer.setMap(null);}
return mapLayer;}
function ebfMapsShowArea(map,lat,lng,radius,typeRadius,title,color,centralize){var miles;if(typeRadius=='km'){miles=radius/1.609;}else{miles=radius;}
var center=new google.maps.LatLng(lat,lng);var placemap={};placemap[title]={center:center,radius:miles};for(var place in placemap){var radiusOptions={strokeColor:color,strokeOpacity:0.8,strokeWeight:2,fillColor:color,fillOpacity:0.35,map:map,center:placemap[place].center,radius:placemap[place].radius*1655};if(centralize==true){map.setCenter(center)}
return new google.maps.Circle(radiusOptions);}}
function ebfMapsStreetView(form,component,map,lat,lng,vertical,horizontal){if(form&&component){var streetview;component=controller.getElementById(component,form);var position=new google.maps.LatLng(lat,lng);var streetOptions={position:position,pov:{heading:vertical,pitch:horizontal}};streetview=new google.maps.StreetViewPanorama(component.div,streetOptions);map.setStreetView(streetview);return streetview;}}
function ebfMapsToggleStreetView(streetview){if(streetview){var toggle=streetview.getVisible();if(toggle==false){streetview.setVisible(true);}else{streetview.setVisible(false);}}}
function ebfMapsTraceRoute(map,addressStart,addressEnd,addressPoints,travelMode,designMarker){var directionsService;var directionsRenderer;var addressPointsAux;if(addressPoints){addressPointsAux='[';for(i=0;i<addressPoints.length;i++){if((i+1)==addressPoints.length){addressPointsAux=addressPointsAux+'{location: \"'+addressPoints[i]+'\"}';}else{addressPointsAux=addressPointsAux+'{location: \"'+addressPoints[i]+'\"},';}}
addressPointsAux=addressPointsAux+']';}
directionsService=new google.maps.DirectionsService();designMarker=designMarker?false:!designMarker;directionsRenderer=new google.maps.DirectionsRenderer({suppressMarkers:designMarker});directionsRenderer.setMap(map);var request={origin:addressStart,destination:addressEnd,waypoints:eval(addressPointsAux),travelMode:travelMode};directionsService.route(request,function(response,status){if(status==google.maps.DirectionsStatus.OK){directionsRenderer.setDirections(response);}});return directionsRenderer;}
function ebfMapsTraceRouteCoordenate(map,latOrigin,lngOrigin,latDestination,lngDestination,addressPoints,travelMode,designMarker){var directionsService;var directionsRenderer;var addressPointsAux;if(addressPoints){addressPointsAux='[';for(i=0;i<addressPoints.length;i++){if((i+1)==addressPoints.length){addressPointsAux=addressPointsAux+'{location: new google.maps.LatLng('+addressPoints[i][0]+', '+addressPoints[i][1]+')}';}else{addressPointsAux=addressPointsAux+'{location: new google.maps.LatLng('+addressPoints[i][0]+', '+addressPoints[i][1]+')}, ';}}
addressPointsAux=addressPointsAux+']';}
directionsService=new google.maps.DirectionsService();designMarker=designMarker?false:!designMarker;directionsRenderer=new google.maps.DirectionsRenderer({suppressMarkers:designMarker});directionsRenderer.setMap(map);var addressStart=new google.maps.LatLng(latOrigin,lngOrigin);var addressEnd=new google.maps.LatLng(latDestination,lngDestination);var request={origin:addressStart,destination:addressEnd,waypoints:eval(addressPointsAux),travelMode:travelMode};directionsService.route(request,function(response,status){if(status==google.maps.DirectionsStatus.OK){directionsRenderer.setDirections(response);}else{return status;}});return directionsRenderer;}
function ebfMarkerAddEventListener(obj,evt,flow,params,eventObject){eventObject=parseBoolean(eventObject);if(eventObject){params.unshift(this);obj.addListener(evt,function(){ebfSetRuleExecutionTime(flow,params,0);});}else{obj.addListener(evt,function(){ebfSetRuleExecutionTime(flow,params,0);});}}
function ebfMaskFormatter(value,mask){var pos=mask.indexOf(";");if(pos!=-1)
mask=mask.substring(0,pos);switch(mask){case"###,#":value=value.replace(/\D/g,"");value=value.replace(/(\d)(\d{1})$/,"$1,$2");break;case"###.##":value=value.replace(/\D/g,"");value=value.replace(/(\d)(\d{2})$/,"$1.$2");break;case"$":value=value.replace(/\D/g,"");value=value.replace(/(\d)(\d{20})$/,"$1.$2");value=value.replace(/(\d)(\d{17})$/,"$1.$2");value=value.replace(/(\d)(\d{14})$/,"$1.$2");value=value.replace(/(\d)(\d{11})$/,"$1.$2");value=value.replace(/(\d)(\d{8})$/,"$1.$2");value=value.replace(/(\d)(\d{5})$/,"$1.$2");value=value.replace(/(\d)(\d{2})$/,"$1,$2");break;case"99\\.999\\-999":value=value.replace(/\D/g,"");if(value.length>8)
value=value.substring(0,8);value=value.replace(/^(\d{2})(\d)/,"$1.$2");value=value.replace(/(\d{3})(\d{3})$/,"$1-$2");break;case"99\\.999\\-\\0\\0\\0":value=value.replace(/\D/g,"");if(value.length>8)
value=value.substring(0,8);if(value.length<8){var length=8-value.length;for(var i=0;i<length;i++)
value=value+'0';}
value=value.replace(/^(\d{5})(\d)/,"$1-$2")
break;case"99\\.999\\.999\\/9999\\-99":value=value.replace(/\D/g,"");if(value.length>14)
value=value.substring(0,14);value=value.replace(/^(\d{2})(\d)/,"$1.$2");value=value.replace(/^(\d{2})\.(\d{3})(\d)/,"$1.$2.$3");value=value.replace(/\.(\d{3})(\d)/,".$1/$2");value=value.replace(/(\d{4})(\d)/,"$1-$2");break;case"999\\.999\\.999\\-99":value=value.replace(/\D/g,"");if(value.length>11)
value=value.substring(0,11);value=value.replace(/(\d{3})(\d)/,"$1.$2");value=value.replace(/(\d{3})(\d)/,"$1.$2");value=value.replace(/(\d{3})(\d{1,2})$/,"$1-$2");break;case"99-99999":value=value.replace(/\D/g,"");if(value.length>7)
value=value.substring(0,7);value=value.replace(/(\d{2})(\d)/,"$1-$2");break;case"99.99.999":value=value.replace(/\D/g,"");if(value.length>7)
value=value.substring(0,7);value=value.replace(/(\d)(\d{5})$/,"$1.$2");value=value.replace(/(\d)(\d{3})$/,"$1.$2");break;case"99.99.99.999.999":value=value.replace(/\D/g,"");if(value.length>12)
value=value.substring(0,12);value=value.replace(/(\d)(\d{10})$/,"$1.$2");value=value.replace(/(\d)(\d{8})$/,"$1.$2");value=value.replace(/(\d)(\d{6})$/,"$1.$2");value=value.replace(/(\d)(\d{3})$/,"$1.$2");break;case"999\\.99999\\.99\\-9":value=value.replace(/\D/g,"");if(value.length>11)
value=value.substring(0,11);value=value.replace(/(\d{3})(\d)/,"$1.$2");value=value.replace(/^(\d{3})\.(\d{5})(\d)/,"$1.$2.$3");value=value.replace(/^(\d{3})\.(\d{5})\.(\d{2})(\d)$/,"$1.$2.$3-$4")
break;case"99999/9999":value=value.replace(/\D/g,"");if(value.length>9)
value=value.substring(0,9);value=value.replace(/(\d)(\d{4})$/,"$1/$2");break;case"9.9.99.99.99.99":value=value.replace(/\D/g,"");if(value.length>10)
value=value.substring(0,10);value=value.replace(/(\d)(\d{9})$/,"$1.$2");value=value.replace(/(\d)(\d{8})$/,"$1.$2");value=value.replace(/(\d)(\d{6})$/,"$1.$2");value=value.replace(/(\d)(\d{4})$/,"$1.$2");value=value.replace(/(\d)(\d{2})$/,"$1.$2");break;case"9.9.99.99.99.99.99":value=value.replace(/\D/g,"");if(value.length>12)
value=value.substring(0,12);value=value.replace(/(\d)(\d{11})$/,"$1.$2");value=value.replace(/(\d)(\d{10})$/,"$1.$2");value=value.replace(/(\d)(\d{8})$/,"$1.$2");value=value.replace(/(\d)(\d{6})$/,"$1.$2");value=value.replace(/(\d)(\d{4})$/,"$1.$2");value=value.replace(/(\d)(\d{2})$/,"$1.$2");break;case"(99) 9999-9999":value=value.replace(/\D/g,"");if(value.length>10)
value=value.substring(0,10);value=value.replace(/^(\d{2})(\d)/g,"($1) $2");value=value.replace(/(\d)(\d{4})$/,"$1-$2");break;case"99":value=value.replace(/\D/g,"");if(value.length>2)
value=value.substring(0,2);break;case"SP":value=value.replace(/\D/g,"");if(value.length>11)
value=value.substring(0,11);value=value.replace(/^(\d{2})(\d)/g,"($1) $2");value=value.replace(/(\d)(\d{4})$/,"$1-$2");break;default:return ebfMaskFormatter_(value,mask);}
return value;}
function ebfMaskFormatter_(_v,_d){var v=_v,m=convertToJsMask(_d);var r="xU#*l",rt=[],nv="",t,x,a=[],j=0,index=0;rx={"x":"A-Za-z","U":"A-ZÀ-Úa-zà-ú","#":"0-9","*":"A-Za-z0-9","l":"A-ZÀ-Úa-zà-ú"};var ry={"x":"A-Za-zÀ-ú","*":"A-Za-zÀ-ú0-9","c":" .,;:%()'{}|?&<>!{}*^_"};var b=[];for(var i=0;i<m.length;i++){x=m.charAt(i);t=(r.indexOf(x)>-1);if(x=="!")x=m.charAt(i++);if((t)||(t&&(rt.length<v.length)))rt[rt.length]="["+rx[x]+"]";a[a.length]={"chr":x,"mask":t};}
if((v.length>0)){for(i=0;i<a.length;i++){if(a[i].mask){while(v.length>0&&!(new RegExp(rt[j])).test(v.charAt(j)))v=(v.length==1)?"":v.substring(1);if(v.length>0){nv+=v.charAt(j);}
j++;if(a[i].chr=="U")nv=nv.setCharAtUpper(nv.length-1,nv);if(a[i].chr=="l")nv=nv.setCharAtLower(nv.length-1,nv);}else nv+=a[i].chr;if((j>v.length))break;}}
return nv;}
function ebfMath10Logarithm(theta){var result=Math.log(toDouble(theta))/Math.log(10);if(isNaN(result)){throw"Argumento inválido para o cálculo do Logaritmo na Base 10.";}
return result;}
function ebfMathArcCosine(theta){var result=Math.acos(toDouble(theta));if(isNaN(result)){throw"Argumento inválido para o cálculo do Arco Cosseno.";}
return result;}
function ebfMathArcSine(theta){var result=Math.asin(toDouble(theta));if(isNaN(result)){throw"Argumento inválido para o cálculo do Arco Seno.";}
return result;}
function ebfMathArcTangent(theta){var result=Math.atan(toDouble(theta));if(isNaN(result)){throw"Argumento inválido para o cálculo do Arco Tangente.";}
return result;}
function ebfMathArrangement(elements,choices){elements=toLong(elements);choices=toLong(choices);var occurrences=elements-choices;return ebfMathFactorial(elements)/ebfMathFactorial(occurrences);}
function ebfMathCeil(theta){var result=Math.ceil(toDouble(theta));if(isNaN(result)){throw"Argumento inválido arredondando o valor para cima.";}
return result;}
function ebfMathCombination(elements,choices){return ebfMathArrangement(elements,choices)/ebfMathFactorial(choices);}
function ebfMathCosine(theta){var result=Math.cos(toDouble(theta));if(isNaN(result)){throw"Argumento inválido para o cálculo do Cosseno.";}
return result;}
function ebfMathCubeRoot(value){value=toDouble(value);var result=Math.pow(value,1/3);if(isNaN(result)){throw"Argumento inválido para o cálculo da Raiz Cúbica.";}
var ceilValue=Math.ceil(result);if(Math.pow(ceilValue,3)==value){return ceilValue;}
var floorValue=Math.floor(result);if(Math.pow(floorValue,3)==value){return floorValue;}
return result;}
function ebfMathELogarithm(theta){var result=Math.log(toDouble(theta));if(isNaN(result)){throw"Argumento inválido para o cálculo do Logaritmo Neperiano.";}
return result;}
function ebfMathFactorial(value){var result=1;value=toLong(value);if(value<0){throw"Argumento inválido no cálculo em análise combinatória.";}
if(value>1){while(value>1){result*=value;value--;}}
return result;}
function ebfMathFloor(theta){var result=Math.floor(toDouble(theta));if(isNaN(result)){throw"Argumento inválido arredondando o valor para baixo.";}
return result;}
function ebfMathNeper(){return Math.E;}
function ebfMathPI(){return Math.PI;}
function ebfMathSine(theta){var result=Math.sin(toDouble(theta));if(isNaN(result)){throw"Argumento inválido para o cálculo do Seno.";}
return result;}
function ebfMathTangent(theta){var result=Math.tan(toDouble(theta));if(isNaN(result)){throw"Argumento inválido para o cálculo da Tangente.";}
return result;}
function ebfMediaLoad(media){if(media instanceof HTMLDivElement){media=media.getElementsByTagName("video")[0]||media.getElementsByTagName("audio")[0];}
if(media instanceof HTMLVideoElement||media instanceof HTMLAudioElement){media.load();}}
function ebfMediaPlay(media){if(media instanceof HTMLDivElement){media=media.getElementsByTagName("video")[0]||media.getElementsByTagName("audio")[0];}
if(media instanceof HTMLVideoElement||media instanceof HTMLAudioElement){media.play();}}
function ebfMemoNewComponent(tabName,posX,posY,width,height,description,value,id,wrap,compContainer,styleCss){var code=getCodComponent();var component=new HTMLMemo(ebfGetSystemID(),ebfGetFormID(),code,posX,posY,width,height,description,value);component.id=(!isNullable(id)?id:reduceVariable(description));component.wrap=!!wrap;component.zindex=3;component.loadComponentTime=0;component.styleCss=styleCss;var tabDiv;var tab=$mainform().d.t.getTabByName(tabName);if(tab){tabDiv=tab.div;}else{tabDiv=d.t.add(tabName);}
d['c_'+code]=component;if(compContainer){component.container=compContainer;compContainer=document.getElementById(compContainer);component.design(compContainer,true);}else{component.design(tabDiv,true);}
setOrderTabDynamically(component);return component;}
function ebfMemoToBasicRichText(form,componentName){var component=$c(componentName,form);if((component instanceof HTMLMemo)&&(!component.isRichText())){component.richText=1;component.richTextLoad();}}
function ebfMenuChangeMode(mode){mainSystemFrame.changeMode=true;let openXHR=function(method,url,async,formdata,callback,params){let xhr=new XMLHttpRequest();xhr.open(method,url,async);xhr.setRequestHeader("Accept","application/javascript,*/*;q=0.9");xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded"+(isSafari?";charset=UTF-8":""));xhr.addEventListener("load",function(){if(xhr.readyState===4){if(xhr.status>=200&&xhr.status<=299){if(callback&&typeof callback==="function"){callback.apply(params&&Array.isArray(params)?params:[]);}}else{console.error(xhr.responseText);}}});xhr.addEventListener("error",function(){console.error(xhr.responseText);});xhr.send(formdata);};openXHR("POST","form.do",true,"sys="+sysCode+"&param=closeForm&formID="+mainform.idForm+
(mainform.WEBRUN_CSRFTOKEN?"&WEBRUN-CSRFTOKEN="+mainform.WEBRUN_CSRFTOKEN:""),function(){openXHR("POST","changeMode.do",true,"sys="+sysCode+"&action=changeMode&mode="+mode+"&back=true",ebfNavRefreshForm);});}
function ebfModaGridColumn(form,gridName,columnName){var values=new Map();var mode=null;var grid=$c(gridName,form);if(!grid){handleException(new Error("Componente "+gridName+" não encontrado"));return;}
var lines=grid.getRowCount()
var rNc=grid.getRealNameColumn(columnName);var ref=grid.iscCanvas;for(var i=0;i<lines;i++){var data=grid.isFiltered?ref.getOriginalData().localData[i]:ref.getDataSource().cacheData[i];var value=parseNumeric(data[rNc]);if(!isNullable(value)){var amount=1;var currentAmount=values.get(value);if(currentAmount!=null){amount=currentAmount+1;}
values.add(value,amount);}}
var repetition=1;for(var i=0;i<values.size;i++){var quantity=values.getValues()[i];if(quantity>repetition){repetition=quantity;mode=values.getKeys()[i];}}
if(repetition==1){mode=null;}
return mode;}
function ebfMultiSelectGetValues(componentName){let component=$c(componentName);return component.selected;}
function ebfMultiSelectSetValues(componentName,values){let component=$c(componentName);let listValues=values.split(",").map(function(el){return el.trim();});for(let i=0;i<component.keys.length;i++){component.unselectOption(component.keys[i]);}
for(let i=0;i<listValues.length;i++){if(component.keys.indexOf(listValues[i])!=-1){component.selectOption(listValues[i]);}}}
function ebfMultiselectClean(componentName){let component=$c(componentName);if(component){component.clean();}else{handleException(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",arguments[0]));}}
function ebfMultiselectPut(componentName,key,value){let component=$c(componentName);if(component){component.add(key,value);}else{handleException(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",arguments[0]));}}
function ebfNavDeleteCurrentRecord(){var nav=$mainform().d.n;if(nav){if(nav.actDeleteSync)
nav.actDeleteSync();else
nav.actDelete();}}
function ebfNavEditCancel(){var nav=$mainform().d.n;if(nav){nav.timeout(nav.actEditCancel,0);}}
function ebfNavEditSaveRecord(){var nav=$mainform().d.n;if(nav){if(nav.actEditSaveSync)
nav.actEditSaveSync();else
nav.actEditSave();}}
function ebfNavEditSaveRecordAsync(){var nav=$mainform().d.n;if(nav){nav.actEditSave();}}
function ebfNavFirstRecord(){var nav=$mainform().d.n;if(nav){if(nav.actFirstSync)
nav.actFirstSync();else
nav.actFirst();}}
function ebfNavGotoRecord(value){var nav=$mainform().d.n;if(nav){if(nav.actGotoSync)
nav.actGotoSync(value);else
nav.actGoto(value);}}
function ebfNavIncludeCancel(){var nav=$mainform().d.n;if(nav){nav.timeout(nav.actIncludeCancel,0);}}
function ebfNavIncludeMoreSaveRecord(){var nav=$mainform().d.n;if(nav){if(nav.actIncludeSaveMoreSync){try{nav.actIncludeSaveMoreSync();}finally{hideWait();}}else{nav.actIncludeSaveMore();}}}
function ebfNavIncludeMoreSaveRecordAsync(){var nav=$mainform().d.n;if(nav){nav.actIncludeSaveMore();}}
function ebfNavIncludeSaveRecord(){var nav=$mainform().d.n;if(nav){if(nav.actIncludeSaveSync)
nav.actIncludeSaveSync();else
nav.actIncludeSave();}}
function ebfNavIncludeSaveRecordAsync(){var nav=$mainform().d.n;if(nav){nav.actIncludeSave();}}
function ebfNavLastRecord(){var nav=$mainform().d.n;if(nav){if(nav.actLastSync)
nav.actLastSync();else
nav.actLast();}}
function ebfNavNextRecord(){var nav=$mainform().d.n;if(nav){if(nav.actNextSync)
nav.actNextSync();else
nav.actNext();}}
function ebfNavPreviousRecord(){var nav=$mainform().d.n;if(nav){if(nav.actPreviousSync)
nav.actPreviousSync();else
nav.actPrevious();}}
function ebfNavRefreshCurrentRecord(){var nav=$mainform().d.n;if(nav){nav.execAjaxEval("refresh");}}
function ebfNavRefreshForm(){parent.location.reload();}
function ebfNavigationFormAddButton(img,caption,func,params,size){if(!size){size=40;}
func=reduceVariable(func,false);d.n.addMainButton("assets/icons/"+img,caption,function(){executeJSRule(ebfGetSystemID(),ebfGetFormID(),func,params)},size);}
function ebfNewImage(aba,posX,posY,width,height,description,value,type,id,hint,compContainer,styleCss){var code=getCodComponent();var component=new HTMLImage(ebfGetSystemID(),ebfGetFormID(),code,posX,posY,width,height,description,value,type,false);component.hasImage=true;component.viewMode='Estender';component.zoomWidth=0;component.zoomHeight=0;component.id=id;component.exhibitionType=2;component.loadComponentTime=0;component.styleCss=styleCss;var container=$mainform().d.t.getTabByName(aba);if(!container){d.t.add(aba);container=$mainform().d.t.getTabByName(aba);}
if(compContainer){component.container=compContainer;compContainer=document.getElementById(compContainer);component.design(compContainer,true);}else{component.design(container.div,true);}
component.setHint(hint);document['c_'+code]=component;}
function ebfNewLine(){var value="";if(existArgs(arguments)){var qtd=arguments[0];while(qtd-->0){value+="\n";}}
return value;}
function ebfNewLineWithEscape(){var value="";if(existArgs(arguments)){var qtd=arguments[0];while(qtd-->0){value+="\r\n";}}
return value;}
function ebfNextFocus(componentAtual){componentAtual=$c(componentAtual);if(typeof(componentAtual)!="undefined"){controller.next(componentAtual,false);}else{controller.focusFirst();}}
function ebfNotification(title,message,icon,image,timer,tag,flow,params){if(Notification.permission==="default"){Notification.requestPermission(function(permission){if(permission==="granted")
notify();else if(permission==="denied")
console.log("Solicitação de permissão bloqueada pelo usuário");});}else if(Notification.permission==="denied"){console.log("Notificação bloqueada pelo usuário");}else{notify();}
function notify(){tag=tag===undefined||tag===null?"":tag;var renotify=tag===""?false:true;timer=timer===undefined||timer===null||timer===""?5000:(timer*1000);var options={body:message,icon:icon,image:image,tag:tag,renotify:renotify}
var notification=new Notification(title,options);notification.onshow=function(){setTimeout(closeNotify,timer,notification)};if(flow){params!==null&&params instanceof Array?params:[];notification.onclick=function(){ebfFlowExecute(flow,params)};}
function closeNotify(notification){notification.close();}}}
function ebfNotificationRequestPermission(){Notification.permission!="default"?null:Notification.requestPermission();}
var DOMEvent=new Array();function ebfObjectEventAssociate(componente,evento,rule,ruleParams){if(typeof(ruleParams)=='undefined'||ruleParams==null){ruleParams='';}
var component=$w(componente);var startsWithOn=/^on(.+)/;var found=evento.match(startsWithOn);if(found!=null&&found!=-1)
evento=RegExp.$1;var _ruleName=rule;var _params=ruleParams;var _sys=sysCode;var _formID=idForm;var func=function(){executeJSRuleNoField(_sys,_formID,_ruleName,_params);}
DOMEvent[evento]=func;addEvent(component,evento,func,true);}
function ebfObjectKeys(object){return Object.keys(object);}
function ebfOnDragInit(componentVar,flag,ruleName,ruleParams){var components=$c(componentVar);if(components){components.setDraggable(flag==undefined?true:flag,components.div.parentElement);if(components.divDragComponent){components.divDragComponent.style.cursor='pointer';components.divDragComponent.style.zIndex=parseInt(components.div.style.zIndex)+1;components.ondragdrop=function(x,y,oldX,oldY,component,mouseDiffX,mouseDiffY,componentDiv){var newList=new Array();newList.push(x);newList.push(y);newList.push(oldX);newList.push(oldY);newList.push(component);newList.push(mouseDiffX);newList.push(mouseDiffY);newList.push(componentDiv);if(ruleName){if(ruleParams){for(var i=0;i<ruleParams.length;i++){newList.push(ruleParams[i]);}}
executeJSRuleNoField(ebfGetSystemID(),ebfGetFormID(),ruleName,newList,false);}};}}}
function ebfOndragEnd(componentName,ruleName,ruleParams){$c(componentName).ondragend=function(comp,div){executeJSRuleNoField(ebfGetSystemID(),ebfGetFormID(),ruleName,ruleParams);};}
function ebfOndragdrop(componentName,ruleName,ruleParams){if($c(componentName))
if($c(componentName).div){$c(componentName).ondragdrop=function(x,y,oldX,oldY,component,mouseDiffX,mouseDiffY,componentDiv){var newList=new Array();newList.push(x);newList.push(y);newList.push(oldX);newList.push(oldY);newList.push(component);newList.push(mouseDiffX);newList.push(mouseDiffY);newList.push(componentDiv);if(!isNullable(ruleParams)){for(var i=0;i<ruleParams.length;i++){newList.push(ruleParams[i]);}}
executeJSRuleNoField(ebfGetSystemID(),ebfGetFormID(),ruleName,newList,false);};}}
function ebfOpenFloatingUrl(pURL,pWindowName,pWindowDescription,pWindowWidth,pWindowHeight,pClass){var formDiv=mainSystemFrame.document.getElementById("WFRIframeForm"+pWindowName);if(formDiv!==null&&formDiv.className.indexOf("WFRIframeForm-Active")===-1){formDiv.style.zIndex=++mainSystemFrame.lastFormZindex;var activeForms=mainSystemFrame.document.getElementsByClassName("WFRIframeForm-Active");if(activeForms.length>0){activeForms[0].getElementsByTagName("iframe")[0].contentWindow.document.getElementsByTagName("iframe")[0].contentWindow.document.activeElement.blur();activeForms[0].className=activeForms[0].className.replace(" WFRIframeForm-Active","");}
formDiv.className+=" WFRIframeForm-Active";}
if(formDiv===null){openFloatingUrl(pURL,pWindowName,pWindowDescription,pWindowWidth,pWindowHeight,pClass);}else if(mainSystemFrame.document.getElementById("Min"+formDiv.id)!==null){mainSystemFrame.document.getElementById("minimizedFloatingDivs").removeChild(mainSystemFrame.document.getElementById("Min"+formDiv.id));formDiv.style.display="";}}
function ebfOpenFormGrid(gridName){if(gridName){var grid=$c(gridName);if(grid.currentRow==-1&&grid.getRowCount()>0){grid.selectRow(0,true);}
grid.timeout(grid.openNormalForm,0);}}
function ebfOpenLogonDigitalCapture(system,dataConnection){openLogonDigitalCapture(system,dataConnection?dataConnection:"");}
function ebfOpenReport(reportID,useForm,filter,title){openWFRReport2(sysCode,reportID,idForm,title?title:reportID,useForm,filter);}
function ebfOpenReportInline(reportID,params,type,popup,local){url="wfrcore";url+="?action=reportOpenExternal&Order=";url+="&localreport="+(local?"ON":"OFF");url+="&nopopup="+(!popup?"true":"false");url+="&sys="+sysCode;url+="&reportID="+URLEncode(reportID,"GET");url+="&exptype="+type;url+="&callfunction=true"
params=URLEncode(params,"GET");if(params!=null){url+=("&"+params.replace(/%3B/g,"&").replace(/%3D/g,'='));}
IframeTransporter(url);}
function ebfOpenReportInlineOrder(reportID,params,order,type,popup,local){url="wfrcore";url+="?action=reportOpenExternal&Order="+URLEncode(order,"GET");url+="&localreport="+(local?"ON":"OFF");url+="&nopopup="+(!popup?"true":"false");url+="&sys="+sysCode;url+="&reportID="+URLEncode(reportID,"GET");url+="&exptype="+type;url+="&callfunction=true";params=URLEncode(params,"GET");if(params!=null){url+=("&"+params.replace(/%3B/g,"&").replace(/%3D/g,'='));}
IframeTransporter(url);}
function ebfOpenRuleDigitalCapture(ruleName){openRuleDigitalCapture(sysCode,idForm,ruleName);}
function ebfOpenRuleDigitalCaptureString(ruleName){openRuleDigitalCapture(sysCode,idForm,ruleName,"string");}
function ebfOpenUrlSameWindow(urlToOpen){window.top.location.href=urlToOpen;}
function ebfOprMod(){var value=0;if(existArgs(arguments)){value=parseNumeric(arguments[0]);for(var i=1;i<arguments.length;i++){var temp=parseNumeric(arguments[i]);value%=temp;}}
return value;}
function ebfPayment(){var result=0.0;if(existArgs(arguments)){result=(parseNumeric(arguments[0])*parseNumeric(arguments[2]))/(1-Math.pow((1/(1+parseNumeric(arguments[2]))),toLong(parseNumeric(arguments[1]))));}
return result;}
function ebfPlayerSetPlaylist(componentName,URLList,add){component=$c(componentName);if(component){if(!add){component.clearPlaylist();}
URLList.map(function(el){component.addMediaToPlaylist(el,"");});}else{interactionError(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",componentName));}}
function ebfPostData(url,postData,throwsException,async,ruleCallback,ruleCallbackError){if(async){postURLAsync(url,postData,throwsException,ruleCallback,ruleCallbackError);}else{return postURL(url,postData,throwsException);}}
function ebfPrevFocus(componentAtual){componentAtual=$c(componentAtual);if(componentAtual){controller.next(componentAtual,true);}else{controller.focusFirst();}}
function ebfPrintDirect(texto,file){var iframe=document.createElement("iframe");iframe.frameBorder=0;iframe.setAttribute("frameborder","no");iframe.setAttribute("border",0);iframe.setAttribute("marginwidth",0);iframe.setAttribute("marginheight",0);iframe.width=0;iframe.height=0;var obj={};obj.file=file;obj.text=texto;iframe.src="printdirect.jsp?sys="+sysCode+"&texto="+URLEncode(ebfToJSString(translateAcentos(JSON.stringify(obj))));document.body.appendChild(iframe);}
function ebfPrintHTMLContent(title,data){var mywindow=window.open('','');if(!title){title="";}
mywindow.document.write('<html><head><title>'+title+'</title>');css=document.getElementsByTagName('link');for(i=0;i<css.length;i++){if(css[i].rel==="stylesheet"){mywindow.document.write('<link rel="stylesheet" href="'+css[i].href+'" type="text/css" />');}}
mywindow.document.write('</head><body >');mywindow.document.write(data.innerHTML);mywindow.document.write('</body></html>');mywindow.document.close();mywindow.print();return true;}
function ebfPrintHTMLContentPage(){window.print();}
function ebfPrompt(dialog,stringDefault){stringDefault=stringDefault||"";return prompt(dialog,stringDefault);}
function ebfPushRegister(onsucess,senderid){function guid(){return s4()+s4()+'-'+s4()+'-'+s4()+'-'+s4()+'-'+s4()+s4()+s4();}
function s4(){return Math.floor((1+Math.random())*0x10000).toString(16).substring(1);}
ebfFlowExecute(onsucess,[guid()]);}
function ebfRSSReload(name,URL,charset){let component=$c(name);if(component){component.setUrl(URL,charset);}else{interactionError(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",name));}}
function ebfRadioGroupAdd(form,component,value,label){var component=$c(component);if(!(isIE||isIE11)){document.getElementsByName("WFRInput"+component.code)[0].remove();}else{var child=document.getElementsByName("WFRInput"+component.code)[0];child.parentElement.removeChild(child);}
component.add(value,label);}
function ebfRadioGroupClean(form,component){var component=$c(component);var size=component.options.length;for(i=0;i<size;i++){component.labels.splice(0,1);component.values.splice(0,1);}
document.getElementsByName("WFRInput"+component.code)[0].remove();component.reDesign();}
function ebfRadioGroupGetSize(form,component){component=$c(component);return component.options.length;}
function ebfRadioGroupNew(aba,posX,posY,width,height,description,value,labels,values,compContainer,styleCss){var code=getCodComponent();var component=new HTMLRadioGroup(ebfGetSystemID(),ebfGetFormID(),code,posX,posY,width,height,description,value,labels,values);component.id=description;component.zindex=3;component.loadComponentTime=0;component.styleCss=styleCss;var container=$mainform().d.t.getTabByName(aba);if(!container){d.t.add(aba);container=$mainform().d.t.getTabByName(aba);}
setOrderTabDynamically(code);if(compContainer){component.container=compContainer;compContainer=document.getElementById(compContainer);component.design(compContainer,true);}else{component.design(container.div,true);}
document['c_'+code]=component;}
function ebfRadioGroupRemoveByLabel(form,component,label){component=$c(component);var idx=arrayIndexOf(component.labels,label);if(idx!=-1){component.options.splice(idx,1);component.values.splice(idx,1);component.labels.splice(idx,1);}else
interactionError(getLocaleMessage("INFO.KEY_ELEMENT_DOES_NOT_EXIST",key));element=document.getElementsByName("WFRInput"+component.code);if(element){element[0].parentNode.removeChild(element[0]);component.reDesign();}
component.reDesign();}
function ebfRadioGroupRemoveItem(form,component,idx){component=$c(component);component.values.splice(idx,1);component.labels.splice(idx,1);element=document.getElementsByName("WFRInput"+component.code);if(element){element[0].parentNode.removeChild(element[0]);component.reDesign();}}
function ebfRadioGroupSetChecked(form,component,idx){var component=$c(component);for(i=0;i<component.options.length;i++){if(component.options[i].value==idx){component.options[i].setChecked(true);}else{component.options[i].setChecked(false);}}}
function ebfRandom(value){return parseInt(parseNumeric(value)*Math.random());}
function ebfReCaptchaGetChallenge(){var challenge=$mainform().document.getElementById("recaptcha_challenge_field");if(challenge){return challenge.value;}}
function ebfReCaptchaGetResponse(){var response=$mainform().document.getElementById("recaptcha_response_field");if(response){return response.value;}}
function ebfReCaptchaRefresh(){if($mainform().Recaptcha){$mainform().Recaptcha.reload();}}
function ebfReCaptchaShow(componentVar,publicKey,privateKey){if($c(componentVar)){var script=document.createElement("script");script.type="text/javascript";script.src="http://www.google.com/recaptcha/api/js/recaptcha_ajax.js";script.onload=function(){Recaptcha.create(publicKey,$c(componentVar).div,{theme:"white",lang:"pt",callback:Recaptcha.focus_response_field});};$c(componentVar).div.style.border="0";$c(componentVar).div.appendChild(script);}}
function searchFormByGUIDRefreshBevelOtherForm(currentForm,GUID){if(currentForm&&currentForm.formGUID==GUID){return currentForm;}
if(currentForm&&currentForm.$mainform()&&currentForm.$mainform().formGUID==GUID){return currentForm.$mainform();}
if(currentForm.children){for(var i=0;i<currentForm.children.length;i++){try{if(currentForm.children[i].$mainform()){if(currentForm.children[i].$mainform().formGUID==GUID){return currentForm.children[i].$mainform();}
var childForm=currentForm.children[i];if(currentForm.children[i].$mainform().d.n.isModal){childForm=childForm.$mainform();}
var returnForm=searchFormByGUIDRefreshBevelOtherForm(childForm,GUID);if(returnForm){return returnForm;}}}catch(e){}}}}
function searchFloatingFormRefreshOtherForm(formGUID){var openFloatingForms;if(isPopup){var mainFormWindow=top.opener;while(mainFormWindow.opener){mainFormWindow=mainFormWindow.opener;}
openFloatingForms=mainFormWindow.mainSystemFrame.document.getElementsByClassName("WFRIframeForm");}else{openFloatingForms=mainSystemFrame.document.getElementsByClassName("WFRIframeForm");}
for(var i=0;i<openFloatingForms.length;i++){var formReference=openFloatingForms[i].children[1].children[1].contentWindow.mainform;if(formReference.formGUID==formGUID){return formReference;}}}
function ebfRefreshBevelOtherForm(form,componentName){var mainWindow=top;while(getOpenerWindow(mainWindow)!=null){var openerWindow=getOpenerWindow(mainWindow);if(openerWindow.mainform&&!isNullable(openerWindow.mainform.sysCode)){mainWindow=openerWindow;}else{break;}}
var formFounded=searchFormByGUIDRefreshBevelOtherForm(mainWindow,form);if(!formFounded){formFounded=searchFloatingFormGet(form);}
if(formFounded){formFounded.mainform.ebfFrameRefreshForm(form,componentName);}}
function ebfRefreshComponentOtherForm(form,component){if(webrunBroadcast){const jsonProperties={};jsonProperties.formGUID=form;jsonProperties.action="wrc";jsonProperties.component=component;jsonProperties.formTarget=decodeURI(mainform.formGUID);webrunBroadcast.postMessage(jsonProperties);}}
function ebfRefreshCurrentRecortParentForm(){if(parent&&parent.frameElement&&parent.frameElement.targetContext){parent.frameElement.targetContext.mainform.d.n.execAjaxEval("refresh");}else if(top.opener){top.opener.mainform.d.n.execAjaxEval("refresh");}else if(parent.opener){parent.opener.mainform.d.n.execAjaxEval("refresh");}}
function ebfRefreshForm(){$mainform().d.n.actRefresh();}
function ebfRefreshFormModal(){$mainform().d.n.execAjaxEval("refresh");}
function ebfRefreshRecord(){$mainform().d.n.execAjaxEval("refresh");}
function ebfRegExpGetMatches(regexp,text){var sub,re,i;regexp+='';text+='';subsequences=[];re=new RegExp(regexp.split('/')[1],regexp.split('/')[2]);for(i=0;;i++){sub=re.exec(text);if(sub===null||i>=re.lastIndex){break;}else{subsequences.push(sub);}}
return subsequences;}
function ebfRegExpReplaceText(regexp,text,replaceText){regexp+='';text+='';replaceText+='';var re=new RegExp(regexp.split('/')[1],regexp.split('/')[2]);return text.replace(re,replaceText);}
function ebfRemoveAccents(text){if(text==null||typeof text=="undefined"){return null;}
return translateAcentos(text);}
function ebfRemoveAllChildsOf(tree,element){return tree.removeAllChildsOf(element);}
function ebfRemoveDefaultValuesButton(){var nav=$mainform().d.n;if(nav){if(nav.btDefaultValues){nav.btDefaultValues.div.style.display="none";}}}
function ebfRemoveELement(tree,element){tree.removeElement(element);}
function ebfRemoveElementFromList(list,idx){if(list){if((idx)&&(list.splice)){list.splice((idx-1),1);}}
return list;}
function ebfRemoveLineBreak(){var value="";if(existArgs(arguments)){value=arguments[0].replace(/(\r\n|\n|\r)/gm,"");}
return value;}
function ebfRemoveOnSelectStart(ComponentName){var c=$c(ComponentName);if(c){if('undefined'!==typeof c.div.onselectstart){c.div.onselectstart=function(){return false;};}else{c.div.onmousedown=function(){return false;};}}}
function ebfRemoveSaveButtons(){var navigation=$mainform().d.n;if(navigation){if(navigation.insButtons[0]!=null){navigation.insButtons[1].setVisible(false);navigation.insButtons[0].setVisible(false);navigation.insButtons[1]=null;navigation.insButtons[0]=null;}else if(navigation.edtButtons[0]!=null){navigation.edtButtons[0].setVisible(false);navigation.edtButtons[0]=null;}}}
function ebfRemoveSaveMoreButton(){var navigation=$mainform().d.n;if((navigation)&&(navigation.insButtons[0]!=null)){if((navigation.insButtons[1]!=null)&&(navigation.insButtons[2]==null)){navigation.insButtons[0].setVisible(false);navigation.insButtons[0]=null;}else if(navigation.insButtons.length==3){navigation.insButtons[0].setVisible(false);navigation.insButtons[0]=null;}}}
function ebfRemoveSessionAttribute(name,global){try{postForceUTF8;}catch(e){var isFirefoxVersionAbove3=false;var firefoxRegExp=new RegExp("firefox/(\\d+)","i");var firefoxRegExpResult=firefoxRegExp.exec(navigator.userAgent);if(firefoxRegExpResult!=null&&firefoxRegExpResult.length>1){try{var version=parseInt(firefoxRegExpResult[1]);if(version>2){isFirefoxVersionAbove3=true;}}catch(e){}}
postForceUTF8=(isFirefoxVersionAbove3||isSafari);}
var content=getContent("sessionManager.do?sys="+sysCode+"&nome="+URLEncode(name,postForceUTF8)+"&global="+global+"&acao=remove");var ajaxReturn=eval(content);if(ajaxReturn){return ajaxReturn;}else{return"";}}
function ebfRemoveSpinner(spinner){if(spinner)spinner.parentElement.removeChild(spinner);}
function ebfReplace(){var value="";if(existArgs(arguments)){value=arguments[0].toString();var valueToFind=arguments[1].toString();var valueToReplace=arguments[2].toString();value=value.replace(valueToFind,valueToReplace);}
return value;}
function ebfReplaceAll(OldString,FindString,ReplaceString){if(!OldString)OldString="";var SearchIndex=0;var NewString="";OldString=OldString.toString();FindString=FindString.toString();ReplaceString=ReplaceString.toString();while(OldString.indexOf(FindString,SearchIndex)!=-1){NewString+=OldString.substring(SearchIndex,OldString.indexOf(FindString,SearchIndex));NewString+=ReplaceString;SearchIndex=(OldString.indexOf(FindString,SearchIndex)+FindString.length);}
NewString+=OldString.substring(SearchIndex,OldString.length);return NewString;}
function ebfReplaceElementFromList(){listReturn=null;if(existArgs(arguments)){listReturn=arguments[0];var position=parseInt(arguments[1])-1;position=Math.max(0,position);position=Math.min(position,(arguments[0].length-1));listReturn[position]=arguments[2];}
return listReturn;}
function ebfRequestGetParameter(str){var c=window.location;var x="";if(c){c=new String(c);var p=c.indexOf(str);if(p>0){var x=c.slice((p+str.length+1),c.length);if(x.indexOf("&")===0){return"";}else{p=(x.indexOf("&")>0)?x.indexOf("&"):x.length;x=x.slice(0,p);return x;}}}
return x;}
function ebfRestCallNew(action,url,ParamsURL,ruleCallback,Params,headerParams,paramBody,charset,ruleCallbackError,paramsRuleError){var data="";action=action.toUpperCase();var xhr=new XMLHttpRequest();xhr.onreadystatechange=function(){if(this.readyState==4){if(this.status==200||this.status==201||this.status==202){if(ruleCallback){var content=convertNonUnicodeChars(this.responseText);Params=Params==null?[]:Params
var jsonReturn={};jsonReturn.headers=getResponseHeaderMap(this);jsonReturn.status="OK";jsonReturn.statusCode=this.status;jsonReturn.result=content;ebfSetElementAtList(Params,jsonReturn,1)
executeRuleFromJS(ruleCallback,Params);}}else{if(ruleCallbackError){var content=convertNonUnicodeChars(this.responseText);paramsRuleError=paramsRuleError==null?[]:paramsRuleError
var jsonReturn={};jsonReturn.headers=getResponseHeaderMap(this);jsonReturn.status="ERROR";jsonReturn.statusCode=this.status;jsonReturn.result=content;ebfSetElementAtList(paramsRuleError,jsonReturn,1)
executeRuleFromJS(ruleCallbackError,paramsRuleError);}}}};if(action=="POST"||action=="PUT"){if(ParamsURL!==undefined&&ParamsURL!=='undefined'&&ParamsURL!==null&&ParamsURL instanceof Map){var paramsMap=ParamsURL.getKeys();for(j=0;j<ParamsURL.size;j++){if(ParamsURL.size>1&&j+1<ParamsURL.size){data+=""+paramsMap[j]+'='+ebfMapGetObject(ParamsURL,paramsMap[j])+'&';}else{data+=""+paramsMap[j]+'='+ebfMapGetObject(ParamsURL,paramsMap[j]);}}}else{data=ParamsURL;}}else{if(ParamsURL!=""&&ParamsURL!==undefined&&ParamsURL!=='undefined'&&ParamsURL!==null){url=url+"?"+ParamsURL;}}
xhr.overrideMimeType('text/plain; charset='+(charset?charset:ENCODING));xhr.open(action,url,true);if(headerParams!==undefined&&headerParams instanceof Map){var paramsHeader=headerParams.getKeys();for(i=0;i<headerParams.size;i++){xhr.setRequestHeader(paramsHeader[i],ebfMapGetObject(headerParams,paramsHeader[i]));}}
xhr.send(data==""?null:data);}
function getResponseHeaderMap(xhr){const headers={};var responseHeaders=xhr.getAllResponseHeaders();if(responseHeaders){responseHeaders.trim().split(/[\r\n]+/).map(function(value){return value.split(/: /)}).forEach(function(keyValue){headers[keyValue[0].trim()]=keyValue[1].trim();});}
return headers;}
function ebfDrawColorPalette(stageID,callback){var listColor=["00","33","66","99","CC","FF"];var table=document.createElement("table");table.border=1;table.cellPadding=0;table.cellSpacing=0;table.style.borderColor="#666666";table.style.borderCollapse="collapse";var tr,td;var color="";var tbody=document.createElement("tbody");for(var i=0;i<listColor.length;i++){tr=document.createElement("tr");for(var x=0;x<listColor.length;x++){for(var y=0;y<listColor.length;y++){color="#"+listColor[i]+listColor[x]+listColor[y];td=document.createElement("td");td.style.width="11px";td.style.height="11px";td.style.background=color;td.color=color;td.style.borderColor="#000";td.style.cursor="pointer";if(typeof(callback)=="function"){td.onclick=function(){callback.apply(this,[this.color]);}}
tr.appendChild(td);}}
tbody.appendChild(tr);}
table.appendChild(tbody);var element=$c(stageID).div;if(element){element.innerHTML='';element.appendChild(table);}
return table;}
function ebfReturnColor(divName,ruleName,ruleParams){ebfDrawColorPalette(divName,function(color){if(!isNullable(ruleName)){var params=new Array();var newList=new Array();newList.push(color);if(!isNullable(ruleParams)){for(var i=0;i<ruleParams.length;i++){newList.push(ruleParams[i]);}}
executeJSRuleNoField(ebfGetSystemID(),ebfGetFormID(),ruleName,newList,false);$c(divName).div.innerHTML='';}
return color;});}
function ebfRichTextInsertTextAtPosition(component,htmlText){var comp=$c(component);if(comp)comp.insertHtmlAtCaret(htmlText);}
function ebfRuleSchedulerNoParent(ruleName,ruleParams,delay){var system=($mainform().d.WFRForm?$mainform().d.WFRForm.sys.value:$mainform().sysCode);var formID=($mainform().d.WFRForm?$mainform().d.WFRForm.formID.value:"");var params=new Array();params.push(system);params.push(formID);params.push(ruleName);if(!isNullable(ruleParams)){params.push(ruleParams);}else{params.push("");}
timeout(executeJSRuleNoField,delay,params);}
function ebfRunFlowAfterOpen(formGUID,FlowName,ruleParams){var values=top.children;if(values&&values.length>0){for(i=0;i<values.length;i++){try{var mainform=values[i].$mainform();if(mainform.formGUID==formGUID){var myOpenForm=values[i].$mainform();}}catch(e){}}}
var elems=$mainform().controller.getAllElements();for(var i=0;i<elems.length;i++){if(elems[i]instanceof HTMLGroupBox){var iframes=elems[i].div.getElementsByTagName("iframe");if(iframes.length>0){var iframe=iframes[0];var mainform=eval(iframe.id).mainform;if(mainform){if(mainform.formGUID==formGUID){var myBevelForm=elems[i].id;}}}}}
_formGUID=formGUID;_FlowName=FlowName;_ruleParams=ruleParams;if(myOpenForm){try{setTimeout(function(){ebfExecuteRuleOnForm(myOpenForm,FlowName,ruleParams);},100);}catch(e){setTimeout(function(){ebfRunFlowAfterOpen(_formGUID,_FlowName,_ruleParams);},100);}}
else if(myBevelForm){try{setTimeout(function(){ebfExecuteRuleOnFormOpenedBevel(ebfGetGUIDActualForm(),myBevelForm,FlowName,ruleParams);},100);}catch(e){setTimeout(function(){ebfRunFlowAfterOpen(_formGUID,_FlowName,_ruleParams);},100);}}
else{setTimeout(function(){ebfRunFlowAfterOpen(_formGUID,_FlowName,_ruleParams);},100);}}
function ebfSQLGetFieldFromForm(form,com){return controller.getElementById(com,form).getValue();}
function ebfSQLGetFormField(){var value="";if(existArgs(arguments)){value=getFormFieldValue(arguments[0]);}
return value;}
function ebfSQLSetFormField(){if(existArgs(arguments)){changeFormFieldValue(arguments[0],arguments[1]);}
return true;}
function ebfScanCode(success,error,types){}
function ebfSearchSubstring(){var indice=0;if(existArgs(arguments)){var value=arguments[0].toString();var valueToFind=arguments[1].toString();indice=value.indexOf(valueToFind);}
return indice!=-1;}
function ebfSelectedTab(){return d.t.getSelectedTab();}
function ebfSendFilePOSTAsync(){console.log('MakerMobile');}
function ebfSetClientFormVariable(name,value){if(!$mainform().__storage){$mainform().__storage={};}
$mainform().__storage[name]=value;}
function ebfSetColorComponent(ComponentName,color,bgcolor){var c=$c(ComponentName);if(color){c.setColor(color);}
if(bgcolor){c.setBGColor(bgcolor);}}
function ebfSetComponentProperty(){if(existArgs(arguments)){var comp=$c(arguments[1]);if(comp){comp[arguments[2]]=arguments[3];}}
return null;}
function ebfSetCookie(cookieName,cookieValue,cookieComment){var today=new Date();var expire=new Date();expire.setTime(today.getTime()+3600000*24);document.cookie=cookieName+"="+escape(cookieValue)
+";expires="+expire.toGMTString();}
function ebfSetElementAtList(list,value,position){if(list){if(position!==null&&position!==undefined){position--;position=Math.max(0,position);position=Math.min(position,list.length);list.splice(position,0,value);}else{list.push(value)}}
return list;}
function ebfSetFlowOnBecomeActive(flow){}
function ebfebfSetFlowOnPushMessage(flow,params){}
function ebfSetFontStyle(tree,font,size,color){tree.font=font;tree.size=size;tree.color=color;tree.setFontStyle();}
function ebfSetHint(ComponentName,text){var c=$c(ComponentName);c.setHint(text);}
function ebfSetIconsHeight(tree,height){tree.setIconsHeight(height);}
function ebfSetImageSrc(componentName,imageData){var imgComp=$c(componentName);if(imgComp.setImageBase64){imgComp.setImageBase64(imageData);}else{imgComp.img.src='data:image/jpeg;base64,'+imageData;imgComp.noImage.style.display='none';imgComp.img.style.display='block';}}
function ebfSetLocalVariable(varName,varValue){return top.document[varName]=varValue;}
function ebfSetLogDebug(){console.log(arguments[0]);}
function ebfSetOnBackPress(){alert("Função disponível apenas no Maker Mobile!");}
function ebfSetRuleExecutionTime(ruleName,ruleParams,delay){var system=($mainform()&&$mainform().d&&$mainform().d.WFRForm?$mainform().d.WFRForm.sys.value:$mainform().sysCode);var formID=($mainform()&&$mainform().d&&$mainform().d.WFRForm?$mainform().d.WFRForm.formID.value:"");var params=new Array();params.push(system);params.push(formID);params.push(ruleName);if(!isNullable(ruleParams)){params.push(ruleParams);}else{params.push("");}
return timeout(executeJSRuleNoField,delay,params);}
function ebfSetRuleOnConnect(){}
function ebfSetRuleOnDisconnect(){}
function ebfSetSessionAttribute(name,value,global){try{postForceUTF8;}catch(e){var isFirefoxVersionAbove3=false;var firefoxRegExp=new RegExp("firefox/(\\d+)","i");var firefoxRegExpResult=firefoxRegExp.exec(navigator.userAgent);if(firefoxRegExpResult!=null&&firefoxRegExpResult.length>1){try{var version=parseInt(firefoxRegExpResult[1]);if(version>2){isFirefoxVersionAbove3=true;}}catch(e){}}
postForceUTF8=(isFirefoxVersionAbove3||isSafari);}
var postData=("sys="+sysCode+"&nome="+URLEncode(name,postForceUTF8)+"&valor="+URLEncode(value,postForceUTF8)+"&global="+global+"&acao=set");var content=postURL("sessionManager.do",postData);return content;}
function ebfShowConfirm(orderOK,title,msg,func,args){}
function ebfShowMainMessage(msg){showMainMessage(msg,null);}
function ebfShowSweetAlert(titulo,mensagem,icone){Swal.fire({icon:icone,title:titulo,html:mensagem});}
function ebfShowTree(tree,view){if(view)
tree.showTree();else
tree.hideTree();}
function ebfSliderNew(tab,posX,posY,width,height,name,startValue,endValue,posStart,enable,visible,accessible,showNumber,precisionDecimal,tips,compContainer){let code=getCodComponent();let component=new HTMLSlider(ebfGetSystemID(),ebfGetFormID(),code,posX,posY,width,height,"","");component.zindex=3;component.Categoria='Maker 3';component.Aba=tab;component.PosicaoX=posX;component.Posicaoy=posY;component.Tamanho=width;component.Altura=height;component.id=name;component.ValorInicio=(startValue!=null&&typeof startValue!="undefined")?startValue:0;component.ValorFim=(endValue!=null&&typeof endValue==="undefined")?endValue:100;component.ValorInicialMarcador=(posStart!=null&&typeof posStart!="undefined")?posStart:0;component.Habilitado=enable;component.Visivel=visible;component.Acessivel=accessible;component.ExibirNumeracao=showNumber;component.Precisao=(precisionDecimal!=null&&typeof precisionDecimal!="undefined")?precisionDecimal:0;component.Dica=tips;component.Container=compContainer;let container=$mainform().d.t.getTabByName(tab);if(!container){d.t.add(tab);container=$mainform().d.t.getTabByName(tab);}
if(compContainer){compContainer=document.getElementById(compContainer);component.design(compContainer,true);}else{component.design(container.div,true);}}
function ebfSliderPanelNew(tab,posX,posY,height,width,name,imageList,visible,enable,acessible,fontSize,time,fontColor,footerColor,compContainer){let code=getCodComponent();let component=new HTMLSliderPanel(ebfGetSystemID(),ebfGetFormID(),code,posX,posY,width,height,"","");if(imageList instanceof Array){let size=imageList.length;let _JSON_URLs={};var _JSON_Instance={sliderpanel:{}};for(var i=0;i<size;i++){let currentList=imageList[i];_JSON_URLs.path=currentList[0]===null?"":currentList[0];_JSON_URLs.description=currentList[1]===null?"":currentList[1];_JSON_URLs.link=currentList[2]===null?"":currentList[2];_JSON_Instance.sliderpanel[i+1]=_JSON_URLs;_JSON_URLs={}}
_JSON_Instance="JSONInstance("+JSON.stringify(_JSON_Instance)+")";}
component.id=name;component.zindex=3;component.Aba=tab;component.Tamanho=width;component.Container=compContainer;component.Categoria='Maker 3';component.Habilitado=enable;component.Acessivel=acessible;component.Nome=name;component.Visivel=visible;component.CorFonteTexto=fontColor;component.CorRodapeAtivo=footerColor;component.TamanhoFonte=fontSize;component.TabelaImagem=_JSON_Instance;component.Tempo=time;component.Altura=height;component.PosicaoY=posX;component.PosicaoX=posY;let container=$mainform().d.t.getTabByName(tab);if(!container){d.t.add(tab);container=$mainform().d.t.getTabByName(tab);}
if(compContainer){compContainer=document.getElementById(compContainer);component.design(compContainer,true);}else{component.design(container.div,true);}}
function ebfSplit(text,caracterSplit){return text.split(caracterSplit);}
function ebfStartMonitoringGPS(){alert("Disponível apenas no Maker Mobile");}
function ebfStartSpinnerSweet(titulo,mensagem){Swal.fire({title:titulo,html:mensagem,allowEscapeKey:false,allowOutsideClick:false,didOpen:()=>{Swal.showLoading()}});}
function ebfStartSpinnerSweetClose(){swal.close();}
function ebfStartsWith(value,startValue){if(!isNullable(value))
return toString(value).startsWith(startValue);return false;}
function ebfStopRuleExecution(msg){document.hasRuleErrors=true;throw new StopRuleExecution(msg);}
function ebfStringReverse(value){var output="";for(i=0;i<=value.length;i++){output=value.charAt(i)+output;}
return output;}
function ebfStringToHTMLString(value){return stringToHTMLString(value);}
function ebfStringToJs(value){return stringToJs(value);}
function ebfStringToXMLString(value){return stringToXMLString(value);}
function ebfSubstring(){var retorno="";if(existArgs(arguments)){var value=arguments[0].toString();var length=value.length;var ini=parseInt(arguments[1])-1;var fim=ini+parseInt(arguments[2]);ini=ini<0?0:ini;fim=fim>length?length:fim;if(!(ini>length||ini>=fim)){try{retorno=value.substring(ini,fim);}catch(ex){}}}
return retorno;}
function ebfSubstringInverse(value,size){var valor=ebfStringReverse(value);valor=ebfSubstring(valor,1,size);valor=ebfStringReverse(valor);return valor;}
function ebfSystemChangeUser(){var win=top;if(parent.opener){win=parent.opener.top;}else if(getOpenerWindow(top)){win=getOpenerWindow(top).top;}
var param=d.WFRForm.sys.value.toString();win.document.location.href="open.do?sys="+param;}
function ebfSystemExit(){var win=top;if(parent.opener){win=parent.opener.top;}else if(getOpenerWindow(top)){win=getOpenerWindow(top).top;}
var param=d.WFRForm.sys.value.toString();win.document.location.href=getAbsolutContextPath()+"?sys="+param+"&back=false&action=logout";return true;}
function ebfTabNew(name,duplicate){var container=$mainform().d.t.getTabByName(name);if(!container||duplicate){if(d.t){d.t.add(name);}}}
function ebfTableChangeCSS(componente,estilo){var componente=$w(componente);if(componente!=null){componente.className=estilo;}}
function ebfTableChangeStyleCSS(componente,estilo){var componente=document.getElementById(componente);if(componente!=null){if(componente){componente.setAttribute("style",estilo);}}}
function ebfTableColumnVisible(idColumn,Visible){var cell=document.getElementById(idColumn);if(Visible){cell.style.display="block";}
else{cell.style.display="none";}}
function ebfTableHTMLAlterLineColor(component,colorLine){var line=document.getElementById(component);line.style.backgroundColor=colorLine;}
function ebfTableRowVisible(idColumn,Visible){var cell=document.getElementById(idColumn);if(Visible==1){cell.style.display="";}
else{cell.style.display="none";}}
function ebfThrowException(message,cause){var ex=new Object();ex.message=message;ex.cause=cause;throw ex;}
function ebfTimeOfDateTime(date){if(date!=null&&date instanceof Date){date.setYear(1900);date.setMonth(0);date.setDate(1);}
return date;}
function ebfTimerCreate(name,form,com){let container=$c(com);if(container){let timer=new HTMLTimer(ebfGetSystemID(),form,getCodComponent(),container.posX,container.posY,container.width,container.height,name);container.div.classList.add("d-none");timer.id=name;timer.parent=container;timer.valorInicial="00:00:00";if(container.decorationChanged)
timer.setDecoration(container.font,container.size,container.weight,container.italic,container.underline,container.strikeout,container.bgColor,container.color);timer.design(container.doc,false);timer.setVisible(container.visible);return timer;}else{interactionError(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",com));}}
function ebfTimerGetTime(componentName,format){let component=$c(componentName);let time=component.getTimerString();switch(format){case'H':time=time.substring(0,2);break;case'M':time=time.substring(3,5);break;case'S':time=time.substring(6);break;}
return time;}
function ebfTimerPause(id){var timer=$c(id);if(timer){timer.pause();}}
function ebfTimerReset(id){var timer=$c(id);if(timer){timer.reset();}}
function ebfTimerStart(id){var timer=$c(id);if(timer){timer.start();}}
function ebfTimerStop(id){var timer=$c(id);if(timer){timer.stop();}}
function ebfToJSString(str){var sb="";if(str!=null){str=str.toString();for(var i=0;i<str.length;i++){c=str.charAt(i);if(c=='\\'){sb+="\\\\";}else if(c=='\''){sb+="\\'";}else if(c=='"'){sb+="\\\"";}else if(c=='\n'){sb+="\\n";}else if(c=='\r'){}else{sb+=c;}}
return sb;}else{return"";}}
function ebfToLocaleDateString(date,locale,format){locale=locale===undefined||locale===null?resources_locale:locale;locale=ebfReplace(locale,"_","-");if(date instanceof Date){try{var options=JSON.parse(format);}catch(e){handleException(new Error("Texto JSON não está em um formato válido"));}
return date.toLocaleDateString(locale,options);}}
function ebfToLowerCase(){var value="";if(existArgs(arguments)){value=arguments[0].toLowerCase();}
return value;}
function ebfToUpperCase(){var value="";if(existArgs(arguments)){value=arguments[0].toUpperCase();}
return value;}
function ebfTranslate(text){if((text==null)||(typeof text=="undefined")||(text==="")){return text;}
var value=text;if(this.translations.findKey(resources_locale)!=-1){var resourcesMap=this.translations.get(resources_locale);if(resourcesMap.findKey(text)!=-1){value=resourcesMap.get(text);}}
try{if(eval("resources_"+resources_locale)&&eval("resources_"+resources_locale)[text]){return eval("resources_"+resources_locale)[text];}}catch(e){}
if((arguments.length>1)&&(arguments[1]!=null)&&(typeof arguments[1]!="undefined")){if(arguments[1]instanceof Array){var params=arguments[1];for(var i=0;i<params.length;i++){var param=params[i];if(param!=null&&typeof param!="undefined"){var regexp=new RegExp("\\{"+(i)+"\\}","g");value=value.replace(regexp,param);}}}else{for(var i=1;i<arguments.length;i++){var param=arguments[i];if(param!=null&&typeof param!="undefined"){var regexp=new RegExp("\\{"+(i-1)+"\\}","g");value=value.replace(regexp,param);}}}}
return value;}
function ebfTreeChangeBorder(tree,borderSize,color){tree.otherDiv.style.border=borderSize+"px solid "+color;}
function ebfTreeGetElementById(tree,id){if(!tree)
throw"O objeto árvore não foi definido!";if(!(tree instanceof HTMLTreeview))
throw"O objeto passado não é do tipo Árvore!";if(!id)
throw"O ID do elemento desejado não pode ser nulo!";return tree.getElement(id);}
function ebfTreeGetElementDBInfo(tree,element){return tree.getElementDBInfo(element);}
function ebfTreeGetElementDesc(tree,element){if(!tree)
throw"O objeto árvore não foi definido";if(!(tree instanceof HTMLTreeview))
throw"O objeto passado não é do tipo Árvore";if(!element)
throw"O objeto passado não é um elemento de uma árvore";try{return element.caption;}catch(e){throw e;}
return-1;}
function ebfTreeGetElementKey(tree,element){if(!tree)
throw"O objeto árvore não foi definido";if(!(tree instanceof HTMLTreeview))
throw"O objeto passado não é do tipo Árvore";if(!element)
throw"O objeto passado não é um elemento de uma árvore";try{var key=tree.getElementDBInfo(element).chave;return key;}catch(e){throw e;}
return-1;}
function ebfTreeSetElementDBInfo(tree,element,arrInfo){tree.setElementDBInfo(element,arrInfo);}
function ebfTreeSetIcon(tree,element,iconFile){tree.setIcon(element,iconFile);}
function ebfTreeviewCollapseElement(element,isRoot){if(isNullable(element)){return;}
if(!isNullable(element._children)){if(!isRoot&&element._children.length>0){element.close();}
for(var i=0;i<element._children.length;i++){ebfTreeviewCollapseElement(element._children[i]);}}}
function ebfTreeviewCollapseAll(formName,componentName){var component=$c(componentName);if(component instanceof HTMLTreeview){component.tree.autoCollapse=false;ebfTreeviewCollapseElement(component.getRoot(),true);}}
function ebfTreeviewElementClose(element){if(element){element.close();}}
function ebfTreeviewExpandElement(element,isRoot){if(isNullable(element)){return;}
if(!isNullable(element._children)){for(var i=0;i<element._children.length;i++){ebfTreeviewExpandElement(element._children[i]);}
if(!isRoot&&element._children.length>0){element.open();}}}
function ebfTreeviewExpandAll(formName,componentName){var component=$c(componentName);if(component instanceof HTMLTreeview){component.tree.autoCollapse=false;ebfTreeviewExpandElement(component.getRoot(),true);}}
function ebfTreeviewFilter(com,filter){$c(com).filter(filter);}
function ebfTrim(){var value="";if(existArgs(arguments)){value=trim(arguments[0]);}
return value;}
function ebfURLDecoder(url,charset){charset=charset===null||charset===undefined?ENCODING:charset;if(charset.toUpperCase()==='ISO-8859-1'){return unescape(url);}else{return decodeURI(url);}}
function ebfURLEncoder(url,charset){charset=charset===null||charset===undefined?ENCODING:charset;if(charset.toUpperCase()==='ISO-8859-1'){return escape(url);}else{return encodeURI(url);}}
function ebfUpdateValueObjectJson(objectJSON,key,value){objectJSON[key]=value instanceof Map?ebfMapToJson(value):value;return objectJSON;}
function ebfUpdateX(componentVar,newPosition){var component=$c(componentVar);if(component){component.updateX(newPosition);}}
function ebfUpdateY(componentVar,newPosition){var component=$c(componentVar);if(component){component.updateY(newPosition);}}
function ebfUploadFile2(url,ruleValidation,ruleName){var securityVersion1=false;try{securityVersion1=(securityVersion=="1");}catch(e){}
if(isNullable(url)||(securityVersion1&&!(/^(\w+-)+\w+$/.test(url))))url="";if(isNullable(ruleName))ruleName="";if(isNullable(ruleValidation))ruleValidation="";var params="";if(arguments.length>3){for(var i=3;i<arguments.length;i++){params+=("&P_"+(i-3)+"="+URLEncode(arguments[i],"GET"));}}
openRuleUpload(sysCode,idForm,ruleName,url,params,ruleValidation,false);}
function ebfUploadMultipleFiles2(url,ruleValidation,ruleName){var securityVersion1=false;try{securityVersion1=(securityVersion=="1");}catch(e){}
if(isNullable(url)||(securityVersion1&&!(/^(\w+-)+\w+$/.test(url))))url="";if(isNullable(ruleName))ruleName="";if(isNullable(ruleValidation))ruleValidation="";var params="";if(arguments.length>3){for(var i=3;i<arguments.length;i++){params+=("&P_"+(i-3)+"="+URLEncode(arguments[i],"GET"));}}
openRuleUpload(sysCode,idForm,ruleName,url,params,ruleValidation,true);}
function ebfUtilReduceVariable(texto,className){return reduceVariable(texto,!parseBoolean(className));}
function ebfValidateTextER(text,regEx){if(regEx==null||typeof regEx=="undefined"||regEx==""){return false;}
var regExp=new RegExp(regEx);return regExp.test(text);}
function ebfWebSocketClientCheckConnection(ws){return ws.readyState;}
function ebfWebSocketClientDisconnect(ws){if(ws.readyState===WebSocket.OPEN)
ws.close();}
function ebfWebSocketClientSendMessage(ws,message){ws.send(message);}
function ebfWebSocketConnectClient(url,flowOnOpen,onOpenParams,flowOnMessage,onMessageParams,flowOnError,onErrorParams,flowOnClose,onCloseParams){ws=new WebSocket(url);ruleOnOpen=flowOnOpen;ruleOnMessage=flowOnMessage;ruleonError=flowOnError;ruleOnClose=flowOnClose;arrayOnOpen=onOpenParams;arrayOnMessage=onMessageParams;arrayOnerror=onErrorParams;arrayOnClose=onCloseParams;ws.onopen=function(){if(ruleOnOpen!=null){if(arrayOnOpen!=null)
arrayOnOpen.splice(0,0,ws);else{arrayOnOpen=[];arrayOnOpen.push(ws);}
ebfFlowExecute(ruleOnOpen,arrayOnOpen);arrayOnOpen=arrayOnOpen.slice(1,arrayOnOpen.length);}}
ws.onmessage=function(evt){if(arrayOnMessage!=null)
arrayOnMessage.splice(0,0,evt.data);else{arrayOnMessage=[];arrayOnMessage.push(evt.data);}
ebfFlowExecute(ruleOnMessage,arrayOnMessage);arrayOnMessage=arrayOnMessage.slice(1,arrayOnMessage.length);}
ws.onerror=function(evt){if(ruleOnerror!=null)
ebfFlowExecute(ruleonError,arrayOnerror);}
ws.onclose=function(){if(ruleOnClose!=null)
ebfFlowExecute(ruleOnClose,arrayOnClose);}
return ws;}
function ebfWhatIsGridModeStatus(grid){var grid=$c(grid);if(!grid)throw"Componente "+grid+" não encontrado";if(grid.editing)return'A';else if(grid.inserting)return'I';else return'N';}
function ebfWindowGetWidth(){return getWindowDimensions().width;}
function ebfWirelessSendText(subject,content){}
function ebfXMLGetAttribute(node,attribute){return node.getAttribute(attribute);}
function ebfXMLGetChildElement(node,childName){var c=node.getElementsByTagName(childName);if(c.length>0)
return c[0];}
function ebfXMLGetChildrenElement(node,childName){if(childName){return node.getElementsByTagName(childName);}
else{return node.childNodes;}}
function ebfXMLGetElementTagName(node){return node.tagName;}
function ebfXMLGetElementValue(node){if(node&&node.firstChild)
return node.firstChild.nodeValue;else
return null;}
function ebfXMLGetParentElement(node){return node.parentNode}
function ebfXMLGetRoot(doc){if(doc)return doc.documentElement;}
function ebfXMLOpen(XMLText){var doc=null;if(document.implementation&&document.implementation.createDocument){var domParser=new DOMParser();doc=domParser.parseFromString(XMLText,'application/xml');fixXMLDocument(doc);return doc;}
else{doc=new ActiveXObject("MSXML2.DOMDocument");doc.loadXML(XMLText);}
return doc;};function ebfXMLToJSON(xml){if(xml!=null&&typeof xml==="string"){var parse=new DOMParser()
xml=parse.parseFromString(xml,'text/xml');var obj={};if(xml.nodeType==1){if(xml.attributes.length>0){obj["@attributes"]={};for(var j=0;j<xml.attributes.length;j++){var attribute=xml.attributes.item(j);obj["@attributes"][attribute.nodeName]=attribute.nodeValue;}}}else if(xml.nodeType==3){obj=xml.nodeValue;}
if(xml.hasChildNodes()){for(var i=0;i<xml.childNodes.length;i++){var item=xml.childNodes.item(i);var nodeName=item.nodeName;if(typeof(obj[nodeName])=="undefined"){obj[nodeName]=ebfXMLToJSON(item);}else{if(typeof(obj[nodeName].length)=="undefined"){var old=obj[nodeName];obj[nodeName]=[];obj[nodeName].push(old);}
obj[nodeName].push(ebfXMLToJSON(item));}}}
return obj;}};function ebfopenLogonDigitalCapture(){openLogonDigitalCapture(ebfGetSystemID());}
function ebfsetSizeFontComponent(ComponentName,s){s=(s?s:11);$c(ComponentName).setSize(s);}
function ebfshortcutReloadSystem(){shortcutReloadSystem(ebfGetFullSystemID());}
function ebgChangeValueGroupBox(ComponentName,HTML){var c=$c(ComponentName);c.div.innerHTML="";c.div.innerHTML=HTML;}
function searchFormByGUIDFormIsOpened(currentForm,GUID){if(currentForm&&currentForm.formGUID==GUID){return currentForm;}
if(currentForm&&currentForm.$mainform()&&currentForm.$mainform().formGUID==GUID){return currentForm.$mainform();}
if(currentForm.children){for(var i=0;i<currentForm.children.length;i++){try{if(currentForm.children[i].$mainform()){if(currentForm.children[i].$mainform().formGUID==GUID){return currentForm.children[i].$mainform();}
var childForm=currentForm.children[i];if(currentForm.children[i].$mainform().d.n.isModal){childForm=childForm.$mainform();}
var returnForm=searchFormByGUIDFormIsOpened(childForm,GUID);if(returnForm){return returnForm;}}}catch(e){}}}}
function searchFloatingFormIsOpenned(formGUID){var openFloatingForms;if(isPopup){var mainFormWindow=top.opener;while(mainFormWindow&&mainFormWindow.opener){mainFormWindow=mainFormWindow.opener;}
if(mainFormWindow.mainSystemFrame)
openFloatingForms=mainFormWindow.mainSystemFrame.document.getElementsByClassName("WFRIframeForm");else
openFloatingForms=[];}else{openFloatingForms=mainSystemFrame.document.getElementsByClassName("WFRIframeForm");}
for(var i=0;i<openFloatingForms.length;i++){var formReference=openFloatingForms[i].children[1].children[1].contentWindow.mainform;if(formReference.formGUID==formGUID){return formReference;}}}
function formIsOpenned(form){if(isNull(form)){return false;}
var mainWindow=top;while(getOpenerWindow(mainWindow)!=null){var openerWindow=getOpenerWindow(mainWindow);if(openerWindow.mainform&&!isNullable(openerWindow.mainform.sysCode)){mainWindow=openerWindow;}else{break;}}
var myForm=searchFormByGUIDFormIsOpened(mainWindow,form);if(myForm){return true;}else{myForm=searchFloatingFormIsOpenned(form);if(myForm){return true;}
return false;}}
function freTextAreaInsertTextoAtCursor(){if(existArgs(arguments)){var component=$c(arguments[0]);var stringToInsert=arguments[1];if(component){var cPos=component.input.__cursorPos;var sText=component.input.value;var firstPart=sText;var secondPart="";if(cPos){firstPart=sText.substring(0,cPos);secondPart=sText.substring(cPos,sText.length);}
component.setValue(firstPart+stringToInsert+secondPart);}
else{handleException(getLocaleMessage("ERROR.COMPONENT_FIELD_NOT_FOUND",arguments[0]));}}}
function __freMonitorarCursor_setCursorPos(tArea){tArea.__cursorPos=__freMonitorarCursor_getCursorPos(tArea);}
function __freMonitorarCursor_getCursorPos(textElement){if(textElement.selectionStart||textElement.selectionStart=='0'){return textElement.selectionStart;}
var sOldText=textElement.value;var objRange=document.selection.createRange();var sOldRange=objRange.text;var sWeirdString='#%~';objRange.text=sOldRange+sWeirdString;objRange.moveStart('character',(0-sOldRange.length-sWeirdString.length));var sNewText=textElement.value;objRange.text=sOldRange;for(i=0;i<=sNewText.length;i++){var sTemp=sNewText.substring(i,i+sWeirdString.length);if(sTemp==sWeirdString){var cursorPos=(i-sOldRange.length);return cursorPos;}}}
function freTextAreaMonitorarCursor(){if(existArgs(arguments)){var component=$c(arguments[0]);if(component){component.input.onchange=function(){__freMonitorarCursor_setCursorPos(this);};component.input.onclick=function(){__freMonitorarCursor_setCursorPos(this);};}
else{alert('Componente não encontrado!');}}}
function getAllComponentNames(){var all=controller.getAllElements();var elems=new Array();for(var i in all){if(typeof(all[i])=='function'||all[i].code==-1||all[i].code==0||all[i].code==undefined||all[i].id==undefined)continue;elems.push(all[i].id);}
return elems;}
function getDayOfWeek(paramDate){var date=toDate(paramDate);return date.getDay()+1;}
function isDiferent(){var value=false;if(existArgs(arguments)){var param1=arguments[0];var param2=arguments[1];if(param1 instanceof Date){var data1=param1;var data2=toDate(param2);if(data1!=null&&data2!=null){value=(data1.compareTo(data2)!=0);}}else if(param1 instanceof Times){var hora1=param1;var hora2=parseTime(param2);if(hora1!=null&&hora2!=null){value=(hora1.compareTo(hora2)!=0);}}else{value=(param1!=param2);}}
return value;}
function isEqual(){var value=false;if(existArgs(arguments)){var param1=arguments[0];var param2=arguments[1];if(param1 instanceof Date){var data1=param1;var data2=toDate(param2);if(data1!=null&&data2!=null){value=(data1.compareTo(data2)==0);}}else if(param1 instanceof Times){var hora1=param1;var hora2=parseTime(param2);if(hora1!=null&&hora2!=null){value=(hora1.compareTo(hora2)==0);}}else{value=(param1==param2);}}
return value;}
function isGreater(value1,value2){var value=false;if(value1!=null&&typeof value1!="undefined"&&value2!=null&&typeof value2!="undefined"){var param1=value1;var param2=value2;if(param1 instanceof Date){var data1=param1;var data2=toDate(param2);if(data1!=null&&data2!=null){value=(data1.compareTo(data2)==1);}}else if(param1 instanceof Times){var hora1=param1;var hora2=parseTime(param2);if(hora1!=null&&hora2!=null){value=(hora1.compareTo(hora2)==1);}}else{value=param1>param2;}}
return value;}
function isGreaterOrEqual(value1,value2){var value=false;if(value1!=null&&typeof value1!="undefined"&&value2!=null&&typeof value2!="undefined"){var param1=value1;var param2=value2;if(param1 instanceof Date){var data1=param1;var data2=toDate(param2);if(data1!=null&&data2!=null){value=(data1.compareTo(data2)==0||data1.compareTo(data2)==1);}}else if(param1 instanceof Times){var hora1=param1;var hora2=parseTime(param2);if(hora1!=null&&hora2!=null){value=(hora1.compareTo(hora2)==0||hora1.compareTo(hora2)==1);}}else{value=param1>=param2;}}
return value;}
function isMinor(value1,value2){var value=false;if(value1!=null&&typeof value1!="undefined"&&value2!=null&&typeof value2!="undefined"){var param1=value1;var param2=value2;if(param1 instanceof Date){var data1=param1;var data2=toDate(param2);if(data1!=null&&data2!=null){value=(data1.compareTo(data2)==-1);}}else if(param1 instanceof Times){var hora1=param1;var hora2=parseTime(param2);if(hora1!=null&&hora2!=null){value=(hora1.compareTo(hora2)==-1);}}else{value=param1<param2;}}
return value;}
function isMinorOrEqual(value1,value2){var value=false;if(value1!=null&&typeof value1!="undefined"&&value2!=null&&typeof value2!="undefined"){var param1=value1;var param2=value2;if(param1 instanceof Date){var data1=param1;var data2=toDate(param2);if(data1!=null&&data2!=null){value=(data1.compareTo(data2)==0||data1.compareTo(data2)==-1);}}else if(param1 instanceof Times){var hora1=param1;var hora2=parseTime(param2);if(hora1!=null&&hora2!=null){value=(hora1.compareTo(hora2)==0||hora1.compareTo(hora2)==-1);}}else{value=param1<=param2;}}
return value;}
function isNull(value){if(value==null){return true;}
if(isTypeOf(value,'ActiveXObject')){return(value==null||typeof value=='undefined');}
return(typeof value=='undefined'||value==''||value.toString()=='NaN');}
function isNullOrEmpty(variavel){return(variavel==null||typeof variavel=='undefined'||trim(variavel+'')==''||variavel.toString()=='NaN');}
function listContainsObject(list,obj){position=0;if(list){for(i=0;i<list.length;i++){if(list[i]==obj){position=i+1;}}}
return position;}
function oprAdd(){var value=0;if(existArgs(arguments)){value=arguments[0];if(value instanceof Date){for(var i=1;i<arguments.length;i++){var temp=toDate(arguments[i]);value.incDay(temp.getDate());}}else if(value instanceof Times){for(var i=1;i<arguments.length;i++){var temp=parseTime(arguments[i]);value.incHour(temp.getHour());}}else{value=parseNumeric(value);for(var i=1;i<arguments.length;i++){var temp=parseNumeric(arguments[i]);value+=temp;}}}
return value;}
function oprAnd(){var value=true;if(existArgs(arguments)){for(var i=0;i<arguments.length;i++){var temp=arguments[i];value=value&&temp;}}
return value;}
function oprAverage(){var average=0.0;if(existArgs(arguments)){var divisor=0.0;var dividendo=arguments.length;for(var i=0;i<arguments.length;i++){var temp=arguments[i];if(temp){divisor+=parseNumeric(temp);}}
average=divisor/dividendo;}
return average;}
function oprBetween(){var between=false;if(existArgs(arguments)){var value=arguments[0];var v1=arguments[1];var v2=arguments[2];if(!isNullable(value)&&!isNullable(v1)&&!isNullable(v2)){if((value instanceof Date)&&(v1 instanceof Date)&&(v2 instanceof Date)){between=value.compareTo(v1)>=0&&value.compareTo(v2)<=0;}else if((value instanceof Times)&&(v1 instanceof Times)&&(v2 instanceof Times)){between=value.compareTo(v1)>=0&&value.compareTo(v2)<=0;}else if((typeof value=="number")&&(typeof v1=="number")&&(typeof v2=="number")){between=value>=v1&&value<=v2;}else{between=value.toString()>=v1.toString()&&value.toString()<=v2.toString();}}}
return between;}
function oprDivide(){var value=0;if(existArgs(arguments)){value=parseNumeric(arguments[0]);for(var i=1;i<arguments.length;i++){var temp=arguments[i];value/=parseNumeric(temp);}}
return value;}
function oprIf(){var value=null;if(existArgs(arguments)){value=arguments[0]?arguments[1]:arguments[2];}
return value;}
function oprMaximum(){var maximum=null;if(existArgs(arguments)){maximum=parseNumeric(arguments[0]);for(var i=0;i<arguments.length;i++){var temp=parseNumeric(arguments[i]);if(temp>maximum){maximum=temp;}}}
return maximum;}
function oprMinimum(){var minimum=null;if(existArgs(arguments)){minimum=parseNumeric(arguments[0]);for(var i=0;i<arguments.length;i++){var temp=parseNumeric(arguments[i]);if(temp<minimum){minimum=temp;}}}
return minimum;}
function oprModulus(){var value=0;if(existArgs(arguments)){value=Math.abs(parseNumeric(arguments[0]));}
return value;}
function oprMultiply(){var value=1.0;if(existArgs(arguments)){for(var i=0;i<arguments.length;i++){var temp=arguments[i];value*=parseNumeric(temp);}}
return value;}
function oprNot(){var value=null;if(existArgs(arguments)){var temp=arguments[0];if(temp!=null){if(typeof temp=="number"){value=-temp;}else if(typeof temp=="boolean"){value=!temp;}else{interactionError("Tipo de parâmetro desconhecido para a operação NOT.");value=temp;}}}
return value;}
function oprOr(){var value=false;if(existArgs(arguments)){for(var i=0;i<arguments.length;i++){var temp=arguments[i];value=temp||value;}}
return value;}
function oprPow(){var value=0;if(existArgs(arguments)){value=Math.pow(parseNumeric(arguments[0]),parseNumeric(arguments[1]));}
return value;}
function oprRound(){var value=0;if(existArgs(arguments)){value=Math.round(parseNumeric(arguments[0]));}
return value;}
function oprSqrt(){var value=0;if(existArgs(arguments)){value=Math.sqrt(parseNumeric(arguments[0]));}
return value;}
function oprSubtract(){var value=0;if(existArgs(arguments)){value=arguments[0];if(value instanceof Date){for(var i=1;i<arguments.length;i++){var temp=toDate(arguments[i]);value.subtractDay(temp.getDate());}}else if(value instanceof Times){for(var i=1;i<arguments.length;i++){var temp=parseTime(arguments[i]);value.subtractHour(temp.getHour());}}else{value=parseNumeric(value);for(var i=1;i<arguments.length;i++){var temp=parseNumeric(arguments[i]);value-=temp;}}}
return value;}
function oprTrunc(){var value=0;if(existArgs(arguments)){value=parseNumeric(arguments[0]).trunc();}
return value;}
function removeNavigator(){controller.removeNavigator();}
function stringToDelphiString(v,ident){if((typeof v=="undefined")||(v==null))return'';v=""+v;var SIZE=67;var strings=new Array();var i=0;var s;do{s=v.substr(i,SIZE);if(s!='')strings.push(s);i+=SIZE;}while(s!='');var r='';for(var i=0;i<strings.length;i++){r+=((ident?ident:'')+convertToDelphiString(strings[i]));if(i!=strings.length-1)
r+='+\r\n';}
if(r=='')
return'\'\'';else
return r;}
function convertToDelphiString(v){var r='';var opened=false;for(var i=0;i<v.length;i++){var code=v.charCodeAt(i);if(code==13)
continue;var especial=!((code>=32&&code<=126&&code!=39));if(especial){if(opened){r+='\'';opened=false;}
if(code==10)
r+='#13#10';else
r+='#'+code;}else{if(!opened){r+='\'';opened=true;}
if(code==39)
r+='\'\'';else
r+=v.charAt(i);if(i==v.length-1&&opened)
r+='\'';}}
return r;}
function toBoolean(value){return parseBoolean(value);}
function toBytes(obj){return obj?obj.toString():"";}
function toDate(value){var toDate=null;if(value instanceof Date){toDate=value;}else{if(value!=null&&(typeof value!="undefined")){var dtExpReg=/^\s*(\d+)[\/\.-](\d+)[\/\.-](\d+)(\s(\d+):(\d+):(\d+))?\s*$/;var dataArr=dtExpReg.exec(value);if(dataArr!=null){var dia=retirarZerosIniciais(dataArr[1]);var mes=retirarZerosIniciais(dataArr[2]);var ano=retirarZerosIniciais(dataArr[3]);var hora=retirarZerosIniciais(dataArr[5]);var minuto=retirarZerosIniciais(dataArr[6]);var segundo=retirarZerosIniciais(dataArr[7]);if(hora!=null&&(typeof hora!="undefined")){toDate=new Date(ano,mes-1,dia,hora,minuto,segundo);}else{toDate=new Date(ano,mes-1,dia,0,0,0);}}}}
return toDate;}
function toDegrees(radians){return(Math.PI*toDouble(radians))/180;}
function toDouble(value){return parseNumeric(value);}
function toLong(){var value=0;if(existArgs(arguments)){value=parseInt(toDouble(arguments[0]));}
return value;}
function toRadians(degrees){return(180*toDouble(degrees))/Math.PI;}
function toString(obj){return isNullable(obj)?"":obj.toString();}