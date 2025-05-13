const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signupForm");
    const loginForm = document.getElementById("loginForm");

    // Signup Form Submission
    signupForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const name = signupForm.querySelector('input[placeholder="Name"]').value.trim();
        const email = signupForm.querySelector('input[placeholder="Email"]').value.trim();
        const password = signupForm.querySelector('input[placeholder="Password"]').value.trim();

        if (!name || !email || !password) {
            alert("Please fill all sign up fields.");
            return;
        }

        fetch("api/signup/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: name, email, password }),
        })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                alert("✅ Registration successful. You can now log in.");
                // Optionally toggle to login form here
            } else {
                alert(`❌ ${data.error}`);
            }
        })
        .catch(err => console.error(err));
    });

    // Login Form Submission
    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const email = loginForm.querySelector('input[placeholder="Email"]').value.trim();
        const password = loginForm.querySelector('input[placeholder="Password"]').value.trim();

        if (!email || !password) {
            alert("Please fill all login fields.");
            return;
        }

        fetch("api/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: email, password }),  // Assuming username is email for login
        })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                alert("✅ Login successful!");
                localStorage.setItem("username", data.username);
                window.location.href = "/";  // Redirect to homepage after login
            } else {
                alert(`❌ ${data.error}`);
            }
        })
        .catch(err => console.error(err));
    });

    // Optional: toggle panel switching
    document.getElementById("login").addEventListener("click", () => {
        document.getElementById("container").classList.remove("right-panel-active");
    });

    document.getElementById("register").addEventListener("click", () => {
        document.getElementById("container").classList.add("right-panel-active");
    });
});
