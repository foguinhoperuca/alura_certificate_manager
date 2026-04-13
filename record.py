import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://gcef.sorocaba.sp.gov.br/")
    page.get_by_role("main").get_by_role("link", name=" Entrar").click()
    page.get_by_role("button", name=" Continuar").click()
    page.get_by_role("textbox", name="Nome de usuário").fill("jecampos")
    page.get_by_role("textbox", name="Senha").click()
    page.get_by_role("textbox", name="Senha").fill("XXX")
    page.get_by_role("textbox", name="Senha").press("Tab")
    page.get_by_role("button", name="Entrar").click()
    page.get_by_role("link", name=" Enviar Certificados").first.click()
    page.get_by_role("textbox", name="Nome do curso").click()
    page.get_by_role("textbox", name="Nome do curso").fill("NOME DO CURSO")
    page.get_by_role("textbox", name="Nome do curso").press("Tab")
    page.get_by_role("textbox", name="Instituição").press("Shift+CapsLock")
    page.get_by_role("textbox", name="Instituição").fill("INSTITUIÇÃo")
    page.get_by_role("textbox", name="Instituição").press("Tab")
    page.get_by_placeholder("Horas").click()
    page.get_by_placeholder("Horas").fill("10")
    page.get_by_placeholder("Min").click()
    page.get_by_placeholder("Min").fill("00")
    page.get_by_placeholder("Min").press("Shift+Home")
    page.get_by_placeholder("Min").fill("00")
    page.get_by_role("button", name="Choose File").dblclick()
    page.get_by_role("button", name="Choose File").set_input_files("000_postgresql_triggers_transacoes_erros_cursores.pdf")
    page.locator("#id_form-0-data_inicio").fill("2025-10-21")
    page.locator("#id_form-0-data_fim").fill("2025-12-17")
    page.locator("#id_form-0-data_emissao").fill("2026-04-10")
    page.get_by_role("button", name=" Adicionar Certificado").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
