import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote
import datetime

# Caminho para salvar os arquivos baixados
DOWNLOAD_PATH = r"C:\Users\Bruno\Downloads\FURNAS"

# Garante a criação do diretório, caso não exista
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

class FaturaTransmissao:
    """
    Classe que representaria a fatura coletada no site.
    Adicione ou remova propriedades conforme sua necessidade.
    """
    def __init__(self):
        self.CodigoFatura = None
        self.DataFatura = None
        self.CodigoEmpresaONS = None
        self.CodigoTransmissoraONS = None
        self.DataCompetencia = None
        self.Valor = None
        # Outras propriedades relevantes...

class WebApiFurnas:
    """
    Classe equivalente à 'WebApiFurnas' em C#.
    """

    # URLs base, similares às do C#:
    URL_DEFAULT = (
        "http://portaldocliente.furnas.com.br/sap/bc/webdynpro/sap/zwda_portalclientes"
        "?sap-client=130&sap-theme=sap_bluecrystal"
    )
    URL_LOGIN = "https://portaldocliente.furnas.com.br/sap/bc/webdynpro/sap/zwda_portalclientes?sap-contextid={0}"
    URL_DOWNLOAD = "https://portaldocliente.furnas.com.br/sap/bc/webdynpro/sap/zwda_portalclientes"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()  # Mantém cookies e estado de sessão

    def get_faturas(self):
        """
        Método principal que replica a lógica do 'GetFaturas()' em C#,
        retornando uma lista de FaturaTransmissao.
        """
        print("[INFO] Iniciando get_faturas()...")
        list_faturas = []
        try:
            # 1) GET inicial (URL_DEFAULT) para capturar HTML e extrair sap_context_id e sap_wd_secure_id
            print("[INFO] Fazendo GET na URL_DEFAULT...")
            response_default = self.session.get(self.URL_DEFAULT)
            print(f"[DEBUG] Status code URL_DEFAULT: {response_default.status_code}")

            if response_default and response_default.text and response_default.status_code == 200:
                html_content = response_default.text

                # Extrai sap-contextid
                sap_context_id = self.get_html_value_dados_fatura(
                    html_content,
                    "sap-contextid",
                    "&#x3d;",
                    "\""
                ).replace("&#x25;", "%").replace("%3a", ":")

                # Extrai sap-wd-secure-id
                sap_wd_secure_id = self.get_html_value_dados_fatura(
                    html_content,
                    "sap-wd-secure-id",
                    "value=\"",
                    "\""
                )

                print(f"[DEBUG] sap_context_id: {sap_context_id}")
                print(f"[DEBUG] sap_wd_secure_id: {sap_wd_secure_id}")

                if not sap_context_id or not sap_wd_secure_id:
                    print("[ERRO] Não foi possível extrair sap_context_id ou sap_wd_secure_id do HTML.")
                    return list_faturas

                # Monta URL de login
                url_login_data = self.URL_LOGIN.format(quote(sap_context_id, safe=''))
                print("[INFO] url_login_data:", url_login_data)

                # -----------------------------------------------------------------------------------
                # Observação: Você PRECISA ajustar 'post_dados' para ter TODOS os parâmetros do site.
                # Abaixo é só um EXEMPLO resumido:
                # -----------------------------------------------------------------------------------
                post_dados_inicial = (
                    f"sap-charset=utf-8&sap-wd-secure-id={sap_wd_secure_id}&"
                    "SAPEVENTQUEUE=ClientInspector_Notify~E002Id~E004WD01..."
                    # ...
                )

                print("[INFO] Fazendo POST inicial para iniciar sessão/etapas de login...")
                response_get_login = self.session.post(url_login_data, data=post_dados_inicial)
                print(f"[DEBUG] Status code POST inicial: {response_get_login.status_code}")

                if response_get_login and response_get_login.text and response_get_login.status_code == 200:
                    soup_login = BeautifulSoup(response_get_login.text, "lxml")

                    # 3) Verifica se existe o botão 'Entrar'
                    btn_entrar = soup_login.find_all("span", text="Entrar")
                    print(f"[DEBUG] Botão 'Entrar' encontrado? {len(btn_entrar) > 0}")
                    if btn_entrar:
                        # Pegamos o elemento pai e seu 'id'
                        btn_entrar_el = btn_entrar[0].parent
                        btn_entrar_id = btn_entrar_el.get('id', '')
                        print(f"[DEBUG] ID do botão 'Entrar': {btn_entrar_id}")

                        # Converte "@" em "~0040" como no C#
                        usuario = self.username.replace("@", "~0040")

                        # -----------------------------------------------------------------------------------
                        # POST para efetivar o login (inserir usuário e senha).
                        # Novamente, isso é APENAS um EXEMPLO. Adicione todos os parâmetros reais.
                        # -----------------------------------------------------------------------------------
                        post_dados_login = (
                            f"sap-charset=utf-8&sap-wd-secure-id={sap_wd_secure_id}&_stateful_=X&SAPEVENTQUEUE="
                            f"ComboBox_Change~E002Id~E004WD2C~E005Value~E004{usuario}~E003~E002ResponseData~E004delta..."
                            f"InputField_Change~E002Id~E004WD32~E005Value~E004{self.password}~E003..."
                            f"Button_Press~E002Id~E004{btn_entrar_id}~E003~E002ResponseData~E004delta~E005ClientAction..."
                        )

                        print("[INFO] Fazendo POST de login (usuário/senha)...")
                        response_login = self.session.post(url_login_data, data=post_dados_login)
                        print(f"[DEBUG] Status code POST login: {response_login.status_code}")

                        if response_login and response_login.text and response_login.status_code == 200:
                            soup_after_login = BeautifulSoup(response_login.text, "lxml")

                            # 5) Localiza abas de empresas/transmissoras
                            tab_panel_empresas = soup_after_login.select("table td.lsTbsPanel2 div[role='tablist']")
                            print("[DEBUG] tab_panel_empresas:", len(tab_panel_empresas))

                            if tab_panel_empresas:
                                tab_panel_id = tab_panel_empresas[0].get('id', '').replace("-panel", "")
                                print(f"[DEBUG] ID do tab_panel: {tab_panel_id}")

                                # Cada <span role='tab'> representa uma aba
                                doc_tab_panel = BeautifulSoup(str(tab_panel_empresas[0]), "lxml")
                                tab_empresas = doc_tab_panel.select("span[role='tab']")
                                print(f"[DEBUG] Quantidade de abas encontradas: {len(tab_empresas)}")

                                # Percorre as abas, começando da 2ª (índice 1), como no C#
                                for x in range(1, len(tab_empresas)):
                                    tab_id = tab_empresas[x].get('id', '').replace("-focus", "")
                                    tab_text = tab_empresas[x].get_text(strip=True)

                                    print(f"[INFO] Selecionando aba {x}: {tab_text}")

                                    # POST para selecionar a aba
                                    post_dados_filter = (
                                        f"sap-charset=utf-8&sap-wd-secure-id={sap_wd_secure_id}"
                                        "&_stateful_=X&SAPEVENTQUEUE="
                                        f"TabStrip_TabSelect~E002Id~E004{tab_panel_id}"
                                        f"~E005ItemId~E004{tab_id}~E005ItemIndex~E0041~E003"
                                        "~E002ResponseData~E004delta~E005ClientAction~E004submit"
                                        "~E003~E002~E003"
                                    )

                                    response_filter = self.session.post(url_login_data, data=post_dados_filter)
                                    print(f"[DEBUG] Status code ao selecionar aba {x}: {response_filter.status_code}")

                                    if response_filter and response_filter.text and response_filter.status_code == 200:
                                        soup_filter = BeautifulSoup(response_filter.text, "lxml")

                                        # Mapeia índices das colunas
                                        tab_columns = self.get_tab_columns(soup_filter)
                                        print("[DEBUG] Colunas mapeadas:", tab_columns)

                                        # Localiza as linhas (TR) com atributo sst='0'
                                        rows_linha = soup_filter.select("table table table table tbody tr[sst='0']")
                                        print(f"[DEBUG] Linhas de fatura encontradas na aba {x}: {len(rows_linha)}")

                                        if rows_linha and len(rows_linha) > 0:
                                            for row_linha in rows_linha:
                                                try:
                                                    columns = row_linha.find_all("td")
                                                    # Se colunas mapeadas não tiverem None, acessamos
                                                    if columns and tab_columns['indexVencimento'] is not None:
                                                        vencimento_text = columns[tab_columns['indexVencimento']].get_text(strip=True)
                                                        emissao_text = columns[tab_columns['indexDataDocumento']].get_text(strip=True) \
                                                            if tab_columns['indexDataDocumento'] is not None else ""
                                                        codigo_fatura = columns[tab_columns['indexNumeroDocumento']].get_text(strip=True) \
                                                            if tab_columns['indexNumeroDocumento'] is not None else ""

                                                        fatura = FaturaTransmissao()
                                                        fatura.CodigoFatura = codigo_fatura
                                                        fatura.DataFatura = self.parse_data(emissao_text)

                                                        # Exemplo extraindo valor
                                                        if tab_columns['indexMontante'] is not None:
                                                            fatura.Valor = columns[tab_columns['indexMontante']].get_text(strip=True)

                                                        # Exemplo de cálculo da DataCompetencia
                                                        data_vencimento = self.parse_data(vencimento_text)
                                                        fatura.DataCompetencia = self.get_competencia_from_data_vencimento(data_vencimento)

                                                        # -- Aqui faria downloads de PDF/XML, etc. --
                                                        # e.g. self.save_boleto_pdf(link_boleto, fatura)

                                                        list_faturas.append(fatura)

                                                except Exception as ex:
                                                    print(f"[ERRO] Falha ao processar linha de fatura: {ex}")
                                    else:
                                        print(f"[ERRO] Não foi possível selecionar a aba {x} corretamente.")
                                # Fim do loop de abas
                            else:
                                print("[AVISO] Não foi possível carregar as abas das transmissoras.")
                        else:
                            print("[ERRO] Não foi possível efetuar o login (resposta vazia ou status != 200).")
                    else:
                        print("[ERRO] Botão 'Entrar' não encontrado no HTML (pós POST inicial).")
                else:
                    print("[ERRO] Falha na etapa inicial do login (resposta vazia ou status != 200).")
            else:
                print(f"[ERRO] GET URL_DEFAULT falhou ou retornou vazio. Status code: {response_default.status_code}")
        except Exception as e:
            print(f"[ERRO] Ocorreu uma exceção geral: {e}")

        print(f"[INFO] Fim do get_faturas(). Total faturas: {len(list_faturas)}")
        return list_faturas

    def get_tab_columns(self, soup):
        """
        Função análoga a GetTabColumns do C#. Retorna um dicionário com o índice de cada coluna.
        """
        tab_columns = {
            'indexNFe': None,
            'indexFatura': None,
            'indexBoleto': None,
            'indexVencimento': None,
            'indexNumeroDocumento': None,
            'indexCliente': None,
            'indexAtribuicao': None,
            'indexDataDocumento': None,
            'indexMontante': None,
            'indexNome': None,
            'indexNumeroNotaFiscal': None,
            'indexXMLNFe': None,
            'indexCodigoONS': None,
        }

        # Seleciona headers (th) na suposta linha de cabeçalho
        columns_titulo = soup.select("table table table table tbody tr[role='rowheader'] th")
        if columns_titulo:
            for i, th in enumerate(columns_titulo):
                texto = th.get_text(strip=True).lower()

                # Faz o mapping baseado no texto, semelhante ao switch no C#
                if "nf-e" in texto:
                    tab_columns['indexNFe'] = i
                elif "fatura" in texto:
                    tab_columns['indexFatura'] = i
                elif "boleto" in texto:
                    tab_columns['indexBoleto'] = i
                elif "vencimento" in texto or texto == "data":
                    tab_columns['indexVencimento'] = i
                elif "nº documento" in texto or "n&#xba;&#x20;documento" in texto:
                    tab_columns['indexNumeroDocumento'] = i
                elif "cliente" in texto:
                    tab_columns['indexCliente'] = i
                elif "atribui" in texto:
                    tab_columns['indexAtribuicao'] = i
                elif "data documento" in texto or "data&#x20;documento" in texto:
                    tab_columns['indexDataDocumento'] = i
                elif "montante" in texto:
                    tab_columns['indexMontante'] = i
                elif "nome" == texto:
                    tab_columns['indexNome'] = i
                elif "nota fiscal" in texto or "nota&#x20;fiscal" in texto:
                    tab_columns['indexNumeroNotaFiscal'] = i
                elif "xml nf-e" in texto or "xml&#x20;nf-e" in texto:
                    tab_columns['indexXMLNFe'] = i
                elif "cod. ons" in texto or "cod.&#x20;ons" in texto:
                    tab_columns['indexCodigoONS'] = i

        return tab_columns

    def get_html_value_dados_fatura(self, html_content, input_id, value_delimiter, value_index_of):
        """
        Réplica simplificada de GetHtmlValueDadosFatura do C#.
        Faz busca via .find() e substring no HTML bruto.
        """
        name_pos = html_content.find(input_id)
        if name_pos == -1:
            return ""
        value_pos = html_content.find(value_delimiter, name_pos)
        if value_pos == -1:
            return ""
        start_pos = value_pos + len(value_delimiter)
        end_pos = html_content.find(value_index_of, start_pos)
        if end_pos == -1:
            return ""
        return html_content[start_pos:end_pos]

    def parse_data(self, data_str):
        """
        Exemplo de conversão de string para data (equivalente a TustUtils.GetDateFromStr).
        Ajuste conforme o formato que o site retorna.
        """
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d.%m.%Y"):
            try:
                return datetime.datetime.strptime(data_str, fmt).date()
            except ValueError:
                continue
        return None

    def get_competencia_from_data_vencimento(self, data_vencimento):
        """
        Exemplo hipotético de como calcular a 'DataCompetencia' a partir de uma data de vencimento.
        Ajuste conforme a lógica necessária no seu negócio.
        """
        if not data_vencimento:
            return None
        # Exemplo: subtrai 1 mês do vencimento
        ano = data_vencimento.year
        mes = data_vencimento.month
        dia = data_vencimento.day
        if mes == 1:
            mes = 12
            ano -= 1
        else:
            mes -= 1

        try:
            return datetime.date(ano, mes, dia)
        except ValueError:
            # Se o dia não existe no mês anterior, pega o último dia do mês, etc.
            return datetime.date(ano, mes, 1)

    def save_boleto_pdf(self, url_pdf, fatura):
        """
        Exemplo de método para baixar e salvar o PDF do boleto em DOWNLOAD_PATH.
        """
        try:
            r = self.session.get(url_pdf)
            if r.status_code == 200:
                filename = os.path.join(DOWNLOAD_PATH, f"Boleto_{fatura.CodigoFatura}.pdf")
                with open(filename, "wb") as f:
                    f.write(r.content)
                print(f"[INFO] Boleto salvo em: {filename}")
            else:
                print("[ERRO] Falha ao baixar boleto. Status:", r.status_code)
        except Exception as ex:
            print("[ERRO] Exceção ao salvar boleto PDF:", ex)

    def save_xml(self, url_xml, fatura):
        """
        Exemplo de método para baixar e salvar o XML da NF-e em DOWNLOAD_PATH.
        """
        try:
            r = self.session.get(url_xml)
            if r.status_code == 200:
                filename = os.path.join(DOWNLOAD_PATH, f"NFe_{fatura.CodigoFatura}.xml")
                with open(filename, "wb") as f:
                    f.write(r.content)
                print(f"[INFO] XML NF-e salvo em: {filename}")
            else:
                print("[ERRO] Falha ao baixar XML. Status:", r.status_code)
        except Exception as ex:
            print("[ERRO] Exceção ao salvar XML da NF-e:", ex)

# ----------------------------------------------------------
# Exemplo de uso (main)
# ----------------------------------------------------------
if __name__ == "__main__":
    # Troque pelo usuário e senha reais
    username = "tust@rioenergy.com.br"
    password = "tustre3430"

    api = WebApiFurnas(username, password)
    faturas = api.get_faturas()

    print("Total de faturas encontradas:", len(faturas))
    for idx, fatura in enumerate(faturas, start=1):
        print(f"{idx}. Fatura: {fatura.CodigoFatura} | Emissão: {fatura.DataFatura} "
              f"| Competência: {fatura.DataCompetencia} | Valor: {fatura.Valor}")
