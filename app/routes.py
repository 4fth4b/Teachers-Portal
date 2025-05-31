from app.controller import (
    main,
    HomeView, RegisterView, LoginView, DashboardView,
    LogoutView, StudentAddAPI, StudentEditAPI, StudentDeleteAPI
)

main.add_url_rule('/', view_func=HomeView.as_view('home'))
main.add_url_rule('/register', view_func=RegisterView.as_view('register'))
main.add_url_rule('/login', view_func=LoginView.as_view('login'))
main.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard'))
main.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))

main.add_url_rule(
    '/add_student', view_func=StudentAddAPI.as_view('add_student'))
main.add_url_rule('/edit_student/<int:student_id>',
                  view_func=StudentEditAPI.as_view('edit_student'))
main.add_url_rule('/delete_student/<int:student_id>',
                  view_func=StudentDeleteAPI.as_view('delete_student'))
