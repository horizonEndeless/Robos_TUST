
<!DOCTYPE html>
<html class="w-100 h-100">
    <head>
        <meta charset="ISO-8859-1">
        <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
        <meta name="viewport" content="width=device-width, user-scalable=yes">
        <link rel="shortcut icon" href="images/images_FAT/IMG_8.gif" type="image/x-icon">
        <link rel="stylesheet" type="text/css" href="assets/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="assets/fontawesome/css/all.min.css">
        <link rel="stylesheet" type="text/css" href="assets/form.css?hash=b971b13f6bde3ee209005bd4dd53931f">
        <script type="text/javascript" src="assets/jquery.min.js"></script>
        <script type="text/javascript" src="assets/bootstrap.min.js"></script>
        <script type="text/javascript">const showMessageAsLegacy = false</script>
        <script type="text/javascript">const messageConfig = {};</script>
        <script type="text/javascript" src="wfr.js"></script>
        <script type="text/javascript" src="wfr_masks.js"></script>
        <script type="text/javascript" src="components/sweetalert/sweetalert.min.js"></script>
        <script type="text/javascript" src="components/HTMLMessage.js"></script>
        <script type="text/javascript">
            function formOnLoadAction() {
                
                if (window.dialogArguments && window.dialogArguments.parentWindow) {
                    var openerWindow = window.dialogArguments.parentWindow;
                    if (!openerWindow.children) openerWindow.children = new Array();
                    try { openerWindow.children.push(window); } catch (e) {console.error(e);}
                }

                if (top.opener) {
                    if (top.opener.children) {
                        if (top.opener.children.indexOf(window) == -1) top.opener.children.push(window);
                    } else {
                        if (!top.opener.parent.children) top.opener.parent.children = new Array();
                        if (top.opener.parent.children.indexOf(window) == -1) top.opener.parent.children.push(window);
                    }
                } else if (mainform.isPopup && !mainform.isPrincipal && !mainform.isLoginForm) {
                    if (!top.$mainform().children) top.$mainform().children = new Array();
                    if (top.$mainform().children.indexOf(window) == -1) top.$mainform().children.push(window);
                }
            }

            var isformcontainer = true;
            var mainframe = null;

            if (opener != null) {
                try {
                    mainframe = opener.mainframe;
                } catch (e) {
                    
                }
            }

            try {
                if (opener && opener.closewindow)
                    opener.close();
            } catch (e) {console.error(e);}

            var sys = 'FAT';
            var isDotNET = true;
            var isTomcat7 = false;
            var isPopup = false;
            var formId = $mainform().URLEncode('{BABB4DBB\-8E36\-4A97\-A999\-8A8602F56C28}');
            var codigo = 'null';
            var codFormComp = 'null';
            var lastFormZindex = 1000;
            var unloaded = false;
            var e_access = false;
            var filter = '';
            var onClose = Boolean('');
            var jsonProperties = JSON.parse('{}');
            var SESSION_ID = 's4e3ydx3ffrmcyeryogvl1an';

            function formOnUnLoadAction() {
                unloaded = !unloaded ? (mainSystemFrame.changeMode ? mainSystemFrame.changeMode : false) : unloaded;
                if (!unloaded) {
                    unloaded = true;
                    try {
                        if (mainform.isPrincipal) closeFormHierarchy(formId);
                        if (closeFormAndChildren) closeFormAndChildren();
                        if (mainform.formOnUnLoadAction) {
                            mainform.disableCloseChildren = true;
                            mainform.formOnUnLoadAction();
                        }
                    } catch(e) { console.error(e); }

                    try {
                        if (mainform.onunload) {
                            let road = "";
                            if(mainSystemFrame.reloadSystem || mainSystemFrame.changeMode) road = 'sys=FAT&param=closeForm&formID='+ formId;
                            else road = 'sys=FAT&param=closeForm&onunload=' + mainform.isPrincipal + '&formID='+ formId;
                            if (filter) road += '&filter=' + filter;
                            road = mainform.WEBRUN_CSRFTOKEN ? (road += "&WEBRUN-CSRFTOKEN=" + mainform.WEBRUN_CSRFTOKEN + "&invalidate=true") : road;
                            if (!mainform.isPrincipal && !mainform.isLoginForm) {
                                if (mainform.isPopup && window.opener) window.opener.postForm('form.do', false, true, road);
                                else mainform.parent.parent.postForm('form.do', false, true, road);
                            } else {
                                postForm('form.do', false, false, road);
                            }
                            mainform.onunload();
                        }
                    } catch(e) { }

                    if (onClose) {
                        try {
                            if (mainform.webrunBroadcast && Object.keys(jsonProperties).length > 0)
                                mainform.webrunBroadcast.postMessage(jsonProperties);
                        } catch (e) { console.error(e); }
                    }

                    try { removeChild(mainform); } catch (e) { console.error(e); }

                    if (opener) {
                        try { opener.removeChild(window); } catch (e) { console.error(e); }
                        try { opener.removeChild(mainform); } catch (e) { console.error(e); }
                    }

                    if (parent) {
                        try { parent.removeChild(window); } catch (e) { console.error(e); }
                        try { parent.removeChild(mainform); } catch (e) { console.error(e); }
                    }

                    window.mainframe = null;

                    if (httpPool) {
                        httpPool.free();
                        httpPool = null;
                    }
                }
            }

            addKeyEvent();

            function changeTitle(t) {
                if (parent && parent.changeTitle && parent != window) parent.changeTitle(t);
                else document.title = t;
            }

            

            function removeLoadingSpinner() {
                document.getElementById("loading").style.display = 'none';
            }
        </script>
    </head>
    <body class="w-100 h-100" onload="formOnLoadAction()" onunload="formOnUnLoadAction()" onbeforeunload="formOnUnLoadAction()">
        <div id="WFRIframeBlockMainForm"></div>
        <div id="loading" style="display: block;"><div class="spinner-border text-primary" role="status"><span class="sr-only">...</span></div></div>
        <iframe onload="removeLoadingSpinner()" src="openform.do?sys=FAT&action=openform&formID=%7bBABB4DBB-8E36-4A97-A999-8A8602F56C28%7d&goto=-1&filter=&scrolling=yes" name="mainform" class="position-absolute border-0 w-100 h-100 m-0 overflow-auto" scrolling="yes"></iframe>
        
    </body>
</html>