
Number.prototype.trunc=function(){return parseInt(this.toString());}
Number.prototype.formatMoney=function(c,d,t){var n=this,c=isNaN(c=Math.abs(c))?2:c,d=d==undefined?".":d,t=t==undefined?",":t,s=n<0?"-":"",i=String(parseInt(n=Math.abs(Number(n)||0).toFixed(c))),j=(j=i.length)>3?j%3:0;return s+(j?i.substr(0,j)+t:"")+i.substr(j).replace(/(\d{3})(?=\d)/g,"$1"+t)+(c?d+Math.abs(n-i).toFixed(c).slice(2):"");};Date.prototype.incDay=function(value){var dateActual=this.getDate();this.setDate(dateActual+value);return this;}
Date.prototype.incMonth=function(value){var monthActual=this.getMonth();this.setMonth(monthActual+value);return this;}
Date.prototype.incYear=function(value){var yearActual=this.getFullYear();this.setFullYear(yearActual+value);return this;}
Date.prototype.subtractDay=function(value){var dateActual=this.getDate();this.setDate(dateActual-value);return this;}
Date.prototype.subtractMonth=function(value){var monthActual=this.getMonth();this.setMonth(monthActual-value);return this;}
Date.prototype.subtractYear=function(value){var yearActual=this.getFullYear();this.setFullYear(yearActual-value);return this;}
Date.prototype.compareTo=function(value){if(!(value instanceof Date)){throw RuleException($mainform().getLocaleMessage("ERROR.IMCOMPATIBLE_TYPE"));}
var compare;if(this.valueOf()>value.valueOf()){compare=1;}else if(this.valueOf()<value.valueOf()){compare=-1;}else{compare=0;}
return compare;}
Date.prototype.toString=function(){function formatToDate(value){if(value.toString().length==1)value="0"+value;return value;}
return formatToDate(this.getDate())+"/"+formatToDate(this.getMonth()+1)+"/"+this.getFullYear()
+" "+formatToDate(this.getHours())+":"+formatToDate(this.getMinutes())+":"+formatToDate(this.getSeconds());}
function Times(hour,minute){this.hour=hour;this.minute=minute;this.second=0;this.millisecond=0;if(arguments.length==4){this.second=arguments[2];this.millisecond=arguments[3];}else if(arguments.length==3){this.second=arguments[2];}
if(arguments[0]&&arguments[1])
this.date=new Date(1980,0,1,this.hour,this.minute,this.second,this.millisecond);}
Times.prototype.fromDate=function(date){this.date=date;this.hour=date.getHours();this.minute=date.getMinutes();this.second=date.getSeconds();return this;}
Times.prototype.getDate=function(){return this.date;}
Times.prototype.getHour=function(){return this.hour;}
Times.prototype.getMinute=function(){return this.minute;}
Times.prototype.getSecond=function(){return this.second;}
Times.prototype.getMillisecond=function(){return this.millisecond;}
Times.prototype.incHour=function(value){var actualHour=this.getDate().getHours();this.getDate().setHours(actualHour+value);this.hour=this.getDate().getHours();}
Times.prototype.incMinute=function(value){var actualMinute=this.getDate().getMinutes();this.getDate().setMinutes(actualMinute+value);this.minute=this.getDate().getMinutes();}
Times.prototype.incSecond=function(value){var actualSecond=this.getDate().getSeconds();this.getDate().setSeconds(actualSecond+value);this.second=this.getDate().getSeconds();}
Times.prototype.incMillisecond=function(value){var actualMillisecond=this.getDate().getMilliseconds();this.getDate().setMilliseconds(actualMillisecond+value);this.millisecond=this.getDate().getMilliseconds();}
Times.prototype.subtractHour=function(value){var actualHour=this.getDate().getHours();this.getDate().setHours(actualHour-value);this.hour=this.getDate().getHours();}
Times.prototype.subtractMinute=function(value){var actualMinute=this.getDate().getMinutes();this.getDate().setMinutes(actualMinute-value);this.minute=this.getDate().getMinutes();}
Times.prototype.subtractSecond=function(value){var actualSecond=this.getDate().getSeconds();this.getDate().setSeconds(actualSecond-value);this.second=this.getDate().getSeconds();}
Times.prototype.subtractMillisecond=function(value){var actualMillisecond=this.getDate().getMilliseconds();this.getDate().setMilliseconds(actualMillisecond-value);this.millisecond=this.getDate().getMilliseconds();}
Times.prototype.compareTo=function(value){if(!value instanceof Times){throw RuleException($mainform().getLocaleMessage("ERROR.IMCOMPATIBLE_TYPE"));}
var compare;var actualTime=new Times(this.getHour(),this.getMinute(),this.getSecond(),this.getMillisecond());var compareTime=new Times(value.getHour(),value.getMinute(),value.getSecond(),value.getMillisecond());if(actualTime.getDate().valueOf()>compareTime.getDate().valueOf()){compare=1;}else if(actualTime.getDate().valueOf()<compareTime.getDate().valueOf()){compare=-1;}else{compare=0;}
return compare;}
Times.prototype.toString=function(){return(this.getDate().maskFormat("HH:MM:ss")+"."+this.getDate().getMilliseconds());}
function parseTime(value){var toTime=null;if(value instanceof Times){toTime=value;}else{if(value!=null&&(typeof value!="undefined")){var dtExpReg=/^\s*(\d{1,2}):(\d{1,2}):(\d{1,2})(\.(\d+))?\s*$/;var dataArr=dtExpReg.exec(value);if(dataArr!=null){var hora=retirarZerosIniciais(dataArr[1]);var minuto=retirarZerosIniciais(dataArr[2]);var segundo=retirarZerosIniciais(dataArr[3]);var milisegundo=retirarZerosIniciais(dataArr[5]);if(milisegundo!=null&&(typeof milisegundo!="undefined")){toTime=new Times(hora,minuto,segundo,milisegundo);}else{toTime=new Times(hora,minuto,segundo);}}}}
return toTime;}
function ebfDateSumDay(){var data=0;if(existArgs(arguments)){data=arguments[0];for(var i=1;i<arguments.lentgh;i++){data.incDay(arguments[i].getDate());}}
return data;}
function ebfDateSumMonth(){var data=0;if(existArgs(arguments)){data=arguments[0];for(var i=1;i<arguments.lentgh;i++){data.incMonth(arguments[i].getMonth());}}
return data;}
function ebfDateSumYear(){var data=0;if(existArgs(arguments)){data=arguments[0];for(var i=1;i<arguments.lentgh;i++){data.incYear(arguments[i].getFullYear());}}
return data;}
function ebfDateSubtractDay(){var data=0;if(existArgs(arguments)){data=arguments[0];for(var i=1;i<arguments.lentgh;i++){data.subtractDay(arguments[i].getDate());}}
return data;}
function ebfDateSubtractMonth(){var data=0;if(existArgs(arguments)){data=arguments[0];for(var i=1;i<arguments.lentgh;i++){data.subtractMonth(arguments[i].getMonth());}}
return data;}
function ebfDateSubtractYear(){var data=0;if(existArgs(arguments)){data=arguments[0];for(var i=1;i<arguments.lentgh;i++){data.subtractYear(arguments[i].getFullYear());}}
return data;}
function ActWarningMessage(){if(existArgs(arguments)){var value=arguments[0];if(arguments[0]!=null&&typeof arguments[0]!="undefined"&&arguments[0].toString){value=arguments[0].toString();}
interactionInfo(value);}
return true;}
function ActErrorMessage(){if(existArgs(arguments)){if(arguments[0]!=null&&typeof arguments[0]!="undefined"&&arguments[0].toString){value=arguments[0].toString();}
throw RuleException(value);}
return true;}
function ActShowProgressBar(msg){ActCloseProgressBar();document.pb=new HTMLProgressBar(d&&d.WFRForm?d.WFRForm.sys.value:sysCode,Math.random()*9999999,msg);document.pb.design();}
function ActIncProgressBar(value){if(document.pb!=null&&!isNullable(value)){document.pb.setPercent(parseFloat(value));}}
function ActCloseProgressBar(){if(document.pb!=null){document.pb.close();document.pb=null;}}
function ActNewWarningMessage(){if(existArgs(arguments)){var title=arguments[0]!==undefined&&arguments[0]!==null?arguments[0].toString():"";var message=arguments[1]!==undefined&&arguments[1]!==null?arguments[1].toString():"";var msgWarning=new parent.mainform.HTMLMessage();msgWarning.showWarningMessage(title,message,arguments[2],arguments[3]);}}
function ActNewSuccessMessage(){if(existArgs(arguments)){var title=arguments[0]!==undefined&&arguments[0]!==null?arguments[0].toString():"";var message=arguments[1]!==undefined&&arguments[1]!==null?arguments[1].toString():"";var msgWarning=new parent.mainform.HTMLMessage();msgWarning.showSuccessMessage(title,message,arguments[2],arguments[3]);}}
function ActNewErrorMessage(){if(existArgs(arguments)){var title=arguments[0]!==undefined&&arguments[0]!==null?arguments[0].toString():"";var message=arguments[1]!==undefined&&arguments[1]!==null?arguments[1].toString():"";throw RuleException(title,message,arguments[2],arguments[3]);}}
function ActNewPromptMessage(){if(existArgs(arguments)){var title=arguments[0]!==undefined&&arguments[0]!==null?arguments[0].toString():"";var message=arguments[1]!==undefined&&arguments[1]!==null?arguments[1].toString():"";var placeHolder=arguments[2]!==undefined&&arguments[2]!==null?arguments[2].toString():undefined;var callOk=arguments[3]!==undefined&&arguments[3]!==null?arguments[3].toString():null;var callCancel=arguments[5]!==undefined&&arguments[5]!==null?arguments[5].toString():null;var msgWarning=new parent.mainform.HTMLMessage();msgWarning.showPromptMessage(title,message,placeHolder,callOk,arguments[4],callCancel,arguments[6],arguments[7]);}}
function ActNewInteractionConfirmMessage(){if(existArgs(arguments)){var title=arguments[0]!==undefined&&arguments[0]!==null?arguments[0].toString():"";var message=arguments[1]!==undefined&&arguments[1]!==null?arguments[1].toString():"";var callOk=arguments[2]!==undefined&&arguments[2]!==null?arguments[2].toString():null;var callCancel=arguments[4]!==undefined&&arguments[4]!==null?arguments[4].toString():null;var msgWarning=new parent.mainform.HTMLMessage();msgWarning.showInteractionConfirmMessage(title,message,callOk,arguments[3],callCancel,arguments[5]);}}
function existArgs(){return arguments.length>0;}
function RuleException(message){this.message=arguments.length>1?arguments[1]:message;this.ruleName=document.ruleNameForException;if(arguments.length>1){return[arguments[0],arguments[1],arguments[2],arguments[3]];}else{return this.message;}}
RuleException.prototype.getFormatedMessage=function(){var message=$mainform().getLocaleMessage("ERROR.RULE_EXECUTION_FAILED");if(this.ruleName){message+=" <b>\""+this.ruleName+"\"</b>";}
if(this.message){message+="\n\n<b>"+$mainform().getLocaleMessage("LABEL.MESSAGE")+":</b> "+this.message;}
return message;}
function StopRuleExecution(message){if(message){alert(message);}}
StopRuleExecution.prototype.stop=function(){return true;}
function handleException(ex,url,line){if(ex instanceof StopRuleExecution||(ex&&ex.stop&&ex.stop())){}else if(ex instanceof RuleException){interactionError(ex.getFormatedMessage());}else if(typeof ex=='string'){interactionErrorOld(ex);}else if(ex instanceof Array){var msgError=new parent.mainform.HTMLMessage();msgError.showErrorMessage(ex[0],ex[1],ex[2],ex[4],ex[3]);}else if(ex!=null&&typeof ex!="undefined"){var message="<b>"+$mainform().getLocaleMessage("LABEL.ERROR")+":</b> "+ex.name+"\n";if(parseInt(ex.number)>0){message+=("<b>"+$mainform().getLocaleMessage("LABEL.LINE")+":</b> "+ex.number+"\n");}
message+=("<b>"+$mainform().getLocaleMessage("LABEL.MESSAGE")+":</b> "+ex.message);interactionError(message,null,null,null,ex.stack);}
document.hasRuleErrors=false;parent.document.hasRuleErrors=false;}
function Rule(parent,sys,formID){this.parent=parent;this.sys=sys;this.formID=formID;}
Rule.prototype.RID=-1;Rule.prototype.ruleName="Undefined";Rule.prototype.functionName="Rule";Rule.prototype.isRule=true;Rule.prototype.checkType=function(value,type){return value;}
Rule.prototype.run=function(){return false;}
Rule.prototype.getRID=function(){return this.RID;}
Rule.prototype.getSystem=function(){return this.sys;}
Rule.prototype.getForm=function(){return this.formID;}
Rule.prototype.getParent=function(){return this.parent;}
Rule.prototype.getRuleName=function(){return this.ruleName;}
Rule.prototype.getFunctionName=function(){return this.functionName;}
Rule.prototype.toString=function(){var value="<b>"+$mainform().getLocaleMessage("LABEL.NAME")+":</b> "+this.ruleName+"\n";value+=("<b>Nome Função:</b> "+this.functionName);return value;}
function executeJS(js){var evalRegexp=/<%=([^%]+)%>/;while(js.search(evalRegexp)!=-1){js=RegExp.leftContext+this.context[RegExp.$1]+RegExp.rightContext;}
var varRegexp=/<%([^%]+)%>/;while(js.search(varRegexp)!=-1){js=RegExp.leftContext+"this.context['"+RegExp.$1+"']"+RegExp.rightContext;}
var func=new Function(js);return func.call(this);}
String.prototype.hashCode=function(){var hash=0;var value=this.toString();var length=value.length;for(var i=0,j=0;i<value.length;i++,j++){hash+=Math.pow((value.charCodeAt(j)*31),--length);}
return hash;}
function translateAcentos(aValue){var CHR_ACENTUADA="àèìòùáéíóúâêîôûãõçñäëïöüÀÈÌÒÙÁÉÍÓÚÂÊÎÔÛÃÕÇÑÄËÏÖÜ";var CHR_NAO_ACENTUADA="aeiouaeiouaeiouaocnaeiouAEIOUAEIOUAEIOUAOCNAEIOU";var idx,idxpos;var result="";for(idx=0;idx<aValue.length;idx++){idxpos=CHR_ACENTUADA.indexOf(aValue.charAt(idx));if(idxpos!=-1){result+=CHR_NAO_ACENTUADA.charAt(idxpos);}
else{result+=aValue.charAt(idx);}}
return result;}
function reduceVariable(texto,notClassName){var value="";if(texto){var regexp=/^\d+|\W/g;texto=texto.toString();if(notClassName){value=trim(translateAcentos(texto.toUpperCase())).replace(/\s/g,"_");if(regexp.test(value)){value=value.replace(regexp,"_");}}else{var specialChar=/\W/g;var startsNumeric=/^[\d\W]+/g;value=translateAcentos(texto);if(specialChar.test(value)){value=value.replace(specialChar," ");}
if(startsNumeric.test(value)){value=value.replace(startsNumeric," ");}
value=firstToUpper(trim(value.replace(/\s{2,}/g," ").replace(/_/g," ")));var spacePosition;while((spacePosition=value.indexOf(" "))!=-1){var aux=value.substring(spacePosition+1);value=value.substring(0,spacePosition)+firstToUpper(aux);}}}
return value;}
var eventMap=new Array();eventMap["aomovimentar"]="dragdrop";eventMap["aoiniciarmovimento"]="dragini";eventMap["aofinalizarmovimento"]="dragend";eventMap["aoredimensionar"]="resize";eventMap["aoiniciarredimensionamento"]="resizeini";eventMap["aofinalizarredimensionamento"]="resizeend";eventMap["aoclicar"]="click";eventMap["aoduploclique"]="dblclick";eventMap["aomodificar"]="change";eventMap["aoentrar"]="focus";eventMap["aosair"]="blur";eventMap["aomudarfococomponente"]="componentselectionchange";eventMap["aopressionardelete"]="delete";eventMap["aofinalizar"]="finalize";eventMap["aopressionartecla"]="keypress";eventMap["aosegurartecla"]="keydown";eventMap["aosoltartecla"]="keyup";function ebfRuleEventAssociate(obj,e,func,params,isJava){if(obj==null){obj=window;}else{obj=controller.verifyComponent(obj);}
if(obj){e=e.replace(/\s+/g,"").toLowerCase();var evt=eventMap[e];if(!evt){var startsWithOn=/^on(.+)/;var found=e.match(startsWithOn);if(found!=null&&found!=-1){e=RegExp.$1;}
evt=e;}
if(obj==window&&evt=='keypress')
evt='keyprezz';if(obj.attachEvent&&!IE){if(typeof func=="string"){var aux=obj.isRule;obj.isRule=true;func=new Function(func);obj.attachEvent(obj,evt,func,obj);obj.isRule=aux;}else{if(isJava){var aux=obj.isRule;obj.isRule=true;obj.attachEvent(obj,evt,func,obj);obj.isRule=aux;}else{obj.attachEvent(obj,evt,func.run,func);}}
if(obj.updateEvent){obj.updateEvent(evt);}}else{var object=new HTMLObject();if(typeof func=="string"){object.attachEvent(obj,evt,func,obj);}else{object.attachEvent(obj,evt,func.run,func);}
if(obj.updateEvent){obj.updateEvent(evt);}}}
return obj;}
function ebfEventRemoveAssociation(obj,e){obj=controller.verifyComponent(obj);if(obj){e=e.replace(/\s+/g,"").toLowerCase();var evt=eventMap[e];if(!evt){var startsWithOn=/^on(.+)/;var found=e.match(startsWithOn);if(found!=null&&found!=-1){e=RegExp.$1;}
evt=e;}
obj['event_'+evt]=null;obj['on'+evt]=null;}
return obj;}
function DebugManager(){this.runningRules=new Map();}
DebugManager.prototype.NOSTATUS=0;DebugManager.prototype.STEPINTO=1;DebugManager.prototype.RESUME=2;DebugManager.prototype.RESUMEALL=3;DebugManager.prototype.STOP=4;DebugManager.prototype.STEPOVER=5;DebugManager.prototype.STEPRETURN=6;DebugManager.prototype.getContext=function(rule){var first=true;var json="{";for(var key in rule.context){if(typeof key=="function"){continue;}
if(!first){json+=", ";}
first=false;json+=("'"+stringToJs(key)+"':");if(isNullable(rule.context[key])){json+="null";}else{var value=rule.context[key];if(IE&&isTypeOf(value,'ActiveXObject')){json+=("'"+"[object Document]"+"'");}else{json+=("'"+stringToJs(value)+"'");}}}
json+="}";return json;}
DebugManager.prototype.startRule=function(rule){var url=("sys="+rule.sys+"&");url+=("formID="+rule.formID+"&");url+=("actionType=startRule&");url+=("parentRID="+(rule.parent?rule.parent.getRID():"")+"&");url+=("contextData="+URLEncode(this.getContext(rule),postForceUTF8)+"&");url+=("ruleName="+URLEncode(rule.ruleName,postForceUTF8));if(ENCODING=="UTF-8"&&isFirefoxVersionAbove3){url+="&decodedParams=true";}
var content=postURL("debugJS.do",url);var obj=eval(content);rule.RID=obj.RID;this.breakPoints=obj.breakPoints;this.currentStatus=obj.currentStatus;this.runningRules.add(rule.getRID(),rule);}
DebugManager.prototype.debug=function(rule,id,description){var debug=true;if(this.currentStatus==this.RESUME||this.currentStatus==this.NOSTATUS){debug=this.findBreakPoint(this.breakPoints,rule.ruleName,id);}else if(this.currentStatus==this.RESUMEALL||this.currentStatus==this.STOP){debug=false;}
if(debug){var url=("sys="+rule.sys+"&");url+=("formID="+rule.formID+"&");url+=("actionType=debug&");url+=("RID="+rule.getRID()+"&");url+=("parentRID="+(rule.parent?rule.parent.getRID():"")+"&");url+=("contextData="+URLEncode(this.getContext(rule),postForceUTF8)+"&");url+=("ruleName="+URLEncode(rule.ruleName,postForceUTF8)+"&");url+=("flowExpressionID="+id+"&");url+=("flowExpressionDescription="+URLEncode(description,postForceUTF8));if(ENCODING=="UTF-8"&&isFirefoxVersionAbove3){url+="&decodedParams=true";}
var postContent=postURL("debugJS.do",url);var obj=eval(postContent);if(obj!=null){var content=obj.content;if(content){var json=eval(content)[0];for(var index in json){if(typeof index=="function"){continue;}
rule.context[index]=json[index];}}
this.breakPoints=obj.breakPoints;this.currentStatus=obj.currentStatus;if(!isNullable(obj.error)){this.stopNow=true;this.errorCause=obj.error;throw this.errorCause;}}}}
DebugManager.prototype.stopRule=function(rule){if(this.stopNow){return false;}
var url=("sys="+rule.sys+"&");url+=("formID="+rule.formID+"&");url+=("actionType=stopRule&");url+=("RID="+rule.getRID()+"&");url+=("parentRID="+(rule.parent?rule.parent.getRID():"")+"&");url+=("ruleName="+URLEncode(rule.ruleName,postForceUTF8));if(ENCODING=="UTF-8"&&isFirefoxVersionAbove3){url+="&decodedParams=true";}
postURL("debugJS.do",url);this.runningRules.remove(rule.getRID());}
DebugManager.prototype.findBreakPoint=function(breakPoints,flowId,expressionId){if(breakPoints&&breakPoints.length>0){for(var index in breakPoints){if(typeof index=="function"){continue;}
var breakPointInfo=breakPoints[index];if(breakPointInfo.flowId==flowId&&breakPointInfo.expressionId==expressionId){return true;}}}
return false;}
DebugManager.prototype.flush=function(){var self=this;var func=function(RID,rule){if(!httpPool){httpPool=new HTTPPool();}
self.stopRule(rule);httpPool.free();httpPool=null;}
this.runningRules.flush(func);}
DebugManager.prototype.toString=function(){return("[DebugManager] Current Status: "+this.currentStatus);}
var debugManager=new DebugManager();var webrunDateFormat=function(){var token=/d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZ]|"[^"]*"|'[^']*'/g,timezone=/\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Times|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g,timezoneClip=/[^-+\dA-Z]/g,pad=function(val,len){val=String(val);len=len||2;while(val.length<len)val="0"+val;return val;};return function(date,mask,utc){var dF=webrunDateFormat;if(arguments.length==1&&Object.prototype.toString.call(date)=="[object String]"&&!/\d/.test(date)){mask=date;date=undefined;}
mask=String(dF.masks[mask]||mask||dF.masks["default"]);if(mask.slice(0,4)=="UTC:"){mask=mask.slice(4);utc=true;}
var _=utc?"getUTC":"get",d=date[_+"Date"](),D=date[_+"Day"](),m=date[_+"Month"](),y=date[_+"FullYear"](),H=date[_+"Hours"](),M=date[_+"Minutes"](),s=date[_+"Seconds"](),L=date[_+"Milliseconds"](),o=utc?0:date.getTimezoneOffset(),flags={d:d,dd:pad(d),ddd:dF.i18n.dayNames[D],dddd:dF.i18n.dayNames[D+7],m:m+1,mm:pad(m+1),mmm:dF.i18n.monthNames[m],mmmm:dF.i18n.monthNames[m+12],yy:String(y).slice(2),yyyy:y,h:H%12||12,hh:pad(H%12||12),H:H,HH:pad(H),M:M,MM:pad(M),s:s,ss:pad(s),l:pad(L,3),L:pad(L>99?Math.round(L/10):L),t:H<12?"a":"p",tt:H<12?"am":"pm",T:H<12?"A":"P",TT:H<12?"AM":"PM",Z:utc?"UTC":(String(date).match(timezone)||[""]).pop().replace(timezoneClip,""),o:(o>0?"-":"+")+pad(Math.floor(Math.abs(o)/60)*100+Math.abs(o)%60,4),S:["th","st","nd","rd"][d%10>3?0:(d%100-d%10!=10)*d%10]};return mask.replace(token,function($0){return $0 in flags?flags[$0]:$0.slice(1,$0.length-1);});};}();webrunDateFormat.masks={"default":"ddd mmm dd yyyy HH:MM:ss",shortDate:"m/d/yy",mediumDate:"mmm d, yyyy",longDate:"mmmm d, yyyy",fullDate:"dddd, mmmm d, yyyy",shortTime:"h:MM TT",mediumTime:"h:MM:ss TT",longTime:"h:MM:ss TT Z",isoDate:"yyyy-mm-dd",isoTime:"HH:MM:ss",isoDateTime:"yyyy-mm-dd'T'HH:MM:ss",isoUtcDateTime:"UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"};webrunDateFormat.i18n={dayNames:["Sun","Mon","Tue","Wed","Thu","Fri","Sat","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],monthNames:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","January","February","March","April","May","June","July","August","September","October","November","December"]};Date.prototype.maskFormat=function(mask,utc){return webrunDateFormat(this,mask,utc);};function InvalidVariant(){}
InvalidVariant.prototype.toString=function(){return"Webrun Native: InvalidVariant";}
function checkJSWrapperRule(sysId,formID,reducedRuleName){try{eval(reducedRuleName+"WRAPPER.prototype.run");return true;}catch(ex){var path=(webrunRulesRootPath+"/"+reducedRuleName+".js?hash="+webrunRulesHash);webrun.include(path);return false;}}
function linkWrapperRule(ruleName){window["run"+ruleName]=function(parent,sys,formID,params){checkJSWrapperRule(sys,formID,ruleName);var rule=new window[ruleName+"WRAPPER"](parent,sys,formID);return rule.run.apply(rule,params);}
window[ruleName]=function(parent,sys,formID){this.parent=parent;this.sys=sys;this.formID=formID;}
window[ruleName].prototype.run=function(){window["run"+ruleName](this.parent,this.sys,this.formID,arguments);}}
function linkWrapperRules(){for(var i=0;i<arguments.length;i++){var ruleName=arguments[i];linkWrapperRule(ruleName);}}
function embedRunFunction(func,owner){var embeddedFunction=function(){}
embeddedFunction.prototype.run=function(){return func.call(owner?owner:this);}
return new embeddedFunction();}