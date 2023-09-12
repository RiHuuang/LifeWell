function redirect() {
    window.location.href = `{{url_for('main_routes')}}`;
}

var delay = 3100;

// Mengalihkan halaman setelah penundaan selesai
setTimeout(redirect, delay);