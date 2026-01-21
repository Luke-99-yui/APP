import flet as ft
import google.generativeai as genai
import os

API_KEY = "AIzaSyAwTX7VRbZVI19oM8O99akUsROXjF93tkg"
genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = (
    "あなたは世界で一番優しいおばあちゃんです。相談者に対し『〜だねぇ』『〜だよ』と穏やかに話し、"
    "どんな悩みも否定せず受け入れてください。最後に温かい一言を添えてください。"
)

def get_model():
    try:
        return genai.GenerativeModel(
            model_name='gemini-1.5-flash', 
            system_instruction=SYSTEM_PROMPT
        )
    except Exception:
        return None

def main(page: ft.Page):
    page.title = "おばあちゃんの相談室"
    page.bgcolor = "#FDF5E6"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    
    page.padding = ft.padding.only(top=10, left=10, right=10, bottom=10)
    page.window_soft_input_mode = ft.WindowSoftInputMode.ADJUST_RESIZE

    model = get_model()
    
    chat_session = model.start_chat(history=[]) if model else None

    chat_history = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=15,
    )

    def send_message(e):
        if not user_input.value or not chat_session:
            return
        
        user_text = user_input.value
        user_input.value = ""
        
        
        chat_history.controls.append(
            ft.Row([
                ft.Container(
                    content=ft.Text(user_text, color="white"),
                    bgcolor="#8D6E63",
                    padding=12,
                    border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_left=15),
                    max_width=300,
                )
            ], alignment=ft.MainAxisAlignment.END)
        )
        
        page.update()

        try:
            user_input.disabled = True
            page.update()

            
            response = chat_session.send_message(user_text)
            
            chat_history.controls.append(
                ft.Row([
                    ft.Container(
                        content=ft.Text(f"おばあちゃん: {response.text}", size=16),
                        bgcolor="#E8F5E9",
                        padding=12,
                        border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_right=15),
                        max_width=300,
                    )
                ], alignment=ft.MainAxisAlignment.START)
            )
        except Exception as ex:
            chat_history.controls.append(
                ft.Text(f"【エラーだよ】: 通信を確認しておくれ。{ex}", color="red", size=12)
            )
        
        user_input.disabled = False
        page.update()
        chat_history.scroll_to(offset=-1, duration=300)

    user_input = ft.TextField(
        hint_text="おばあちゃんに相談する...", 
        expand=True, 
        border_radius=25,
        on_submit=send_message,
        bgcolor=ft.colors.WHITE,
        content_padding=15,
    )

    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color="#5D4037",
        bgcolor="#A5D6A7",
        on_click=send_message,
    )

    page.add(
        ft.SafeArea(
            content=ft.Column([
                ft.Row([
                    ft.Text("👵 おばあちゃんの相談室", size=22, weight="bold", color="#5D4037")
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=1, color="#D7CCC8"),
                chat_history,
                ft.Container(
                    content=ft.Row([user_input, send_button], spacing=10),
                    padding=ft.padding.only(bottom=10)
                )
            ], expand=True)
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
