import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("graduation-cap", class_name="h-12 w-12 text-white mb-4"),
                    rx.el.h1(
                        "Teacher's Portal",
                        class_name="text-4xl font-bold text-white mb-4",
                    ),
                    rx.el.p(
                        "Manage your classroom, grades, and student progress efficiently in one place.",
                        class_name="text-blue-100 text-lg max-w-md",
                    ),
                    class_name="z-10 relative",
                ),
                rx.el.div(
                    class_name="absolute inset-0 bg-gradient-to-br from-violet-600 to-indigo-900 opacity-90"
                ),
                rx.el.img(
                    src="https://images.unsplash.com/photo-1497633762265-9d179a990aa6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2073&q=80",
                    class_name="absolute inset-0 w-full h-full object-cover mix-blend-overlay",
                ),
                class_name="hidden lg:flex flex-col justify-center items-center p-12 w-1/2 relative overflow-hidden",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Welcome back",
                            class_name="text-3xl font-bold text-gray-900 mb-2",
                        ),
                        rx.el.p(
                            "Please enter your details to sign in.",
                            class_name="text-gray-500 mb-8",
                        ),
                        rx.cond(
                            AuthState.error_message != "",
                            rx.el.div(
                                rx.icon(
                                    "badge_alert",
                                    class_name="h-5 w-5 text-red-500 mr-2",
                                ),
                                rx.el.span(
                                    AuthState.error_message,
                                    class_name="text-sm text-red-600 font-medium",
                                ),
                                class_name="bg-red-50 border border-red-100 rounded-lg p-4 flex items-center mb-6 animate-fade-in",
                            ),
                        ),
                        rx.el.form(
                            rx.el.div(
                                rx.el.label(
                                    "Email Address",
                                    class_name="block text-sm font-semibold text-gray-700 mb-2",
                                ),
                                rx.el.input(
                                    type="email",
                                    name="email",
                                    placeholder="demo@teacher.com",
                                    required=True,
                                    class_name="w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:border-violet-500 focus:ring-2 focus:ring-violet-200 outline-none transition-all text-gray-900 placeholder-gray-400",
                                ),
                                class_name="mb-5",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Password",
                                    class_name="block text-sm font-semibold text-gray-700 mb-2",
                                ),
                                rx.el.input(
                                    type="password",
                                    name="password",
                                    placeholder="••••••••",
                                    required=True,
                                    class_name="w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:border-violet-500 focus:ring-2 focus:ring-violet-200 outline-none transition-all text-gray-900 placeholder-gray-400",
                                ),
                                class_name="mb-8",
                            ),
                            rx.el.button(
                                rx.cond(
                                    AuthState.is_loading,
                                    rx.el.div(
                                        rx.spinner(
                                            size="2", class_name="text-white mr-2"
                                        ),
                                        "Signing in...",
                                        class_name="flex items-center justify-center",
                                    ),
                                    "Sign In",
                                ),
                                type="submit",
                                disabled=AuthState.is_loading,
                                class_name="w-full py-3.5 rounded-xl bg-violet-600 text-white font-semibold hover:bg-violet-700 active:bg-violet-800 transition-all shadow-lg shadow-violet-200 disabled:opacity-70 disabled:cursor-not-allowed",
                            ),
                            on_submit=AuthState.login,
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Don't have an account? ", class_name="text-gray-500"
                            ),
                            rx.el.a(
                                "Create account",
                                href="/register",
                                class_name="text-violet-600 font-semibold hover:text-violet-700 hover:underline transition-colors",
                            ),
                            class_name="mt-8 text-center text-sm",
                        ),
                    ),
                    class_name="w-full max-w-md",
                ),
                class_name="w-full lg:w-1/2 flex items-center justify-center p-8 bg-white",
            ),
            class_name="flex min-h-screen w-full bg-white",
        ),
        class_name="font-['Inter']",
    )