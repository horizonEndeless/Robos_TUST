
<!DOCTYPE html>
<html class="w-100 h-100">
    <head>
        <meta charset="ISO-8859-1">
        <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
        <meta name="viewport" content="width=device-width, user-scalable=yes">
        <link rel="shortcut icon" href="images/images_FAT/IMG_8.gif" type="image/x-icon">
        <link rel="stylesheet" type="text/css" href="assets/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="assets/form.css?hash=b971b13f6bde3ee209005bd4dd53931f">
        <script type="text/javascript" src="wfr.js"></script>
        <script type="text/javascript" src="rulesFunctions.js"></script>
        <webrun:import src="components/sweetalert/sweetalert.min.js"/>
        <script type="text/javascript" src="components/HTMLMessage.js?hash=30324577082526a1ba48b820bc39107e"></script>
        <script type="text/javascript">const showMessageAsLegacy = false</script>
        <script type="text/javascript">
            let jsonMessage;
            function systemOnLoadAction() {
                if (mainsystem.sysOnLoad) {
                    mainsystem.sysOnLoad();
                }
                systemConnectWebsocket();
            }

            var unloaded = false;
            function systemOnUnLoadAction() {
                if (!unloaded) {
                    unloaded = true;
                    if (mainsystem.sysOnUnLoad) mainsystem.sysOnUnLoad();
                    if (mainsystem.formOnUnLoadAction) mainsystem.formOnUnLoadAction();
                    get('closesystem.do?sys=FAT');
                    closeParents();
                }
            }

            function changeTitle(t) {
                document.title = t;
            }

            /**
            * Função responsável por gerenciar a conexão do usuário com servidor Websocket;
            * @autor Janpier
            * @param reconnect - Indica se é para o usuário se reconectar ao socket.
            */
            function systemConnectWebsocket(reconnect) {
                window.webrunSocket = new WebSocket(getEndpointWS());

                window.webrunSocket.onopen = (event) => {
                    let sendMessage = {};
                    sendMessage.sysCode = "FAT";
                    sendMessage.sessionID = "s4e3ydx3ffrmcyeryogvl1an";
                    if (reconnect) sendMessage.userId = jsonMessage.userId;
                    window.webrunSocket.send(JSON.stringify(sendMessage));
                };

                window.webrunSocket.onclose = (event) => {
                    console.log('Socket closed');
                };

                window.webrunSocket.onerror = (err) => {
                    console.error('Socket encountered error: ', err.message);
                };

                window.webrunSocket.onmessage = (event) => {
                    if (event.data) {
                        try {
                            jsonMessage = JSON.parse(event.data);
                        } catch (e) {
                            console.error(e);
                        }
                    }
                };
            }

            

            /**
            * Associa o evento para verificação se o usuário está conectado a internet.
            * @autor Janpier
            */
            window.addEventListener('online', (event) => {
                

                systemConnectWebsocket(true);
            });

            /**
             * Obtém o endpoint para conexão com o socket
             */
            function getEndpointWS () {
                let endpoint = getAbsolutContextPath();
                endpoint = endpoint.startsWith('https') ? endpoint.replace('https', 'wss') : endpoint.replace('http', 'ws');
                endpoint = endpoint + '/' + 'wss://harpixfat.mezenergia.com/FAT/WS7930705';
                return endpoint;
            }

            function remainSession() {
                try { httpPool.processAsyncGet('remainSession.do?sys=FAT&datetime=' + (new Date().getMilliseconds())); } catch(e) { }
                setTimeout(remainSession, 60000);
            }

            setTimeout(remainSession, 60000);
        </script>
    </head>
    <body class="w-100 h-100" onload="systemOnLoadAction()" onunload="systemOnUnLoadAction()" onbeforeunload="systemOnUnLoadAction()">
        <iframe src="form.jsp?sys=FAT&action=openform&formID=500000435&mode=-1&goto=-1&filter=&scrolling=False&firstLoad=true" name="mainsystem" class="position-absolute border-0 w-100 h-100 m-0 overflow-auto" scrolling="no" noresize></iframe>
    </body>
</html>