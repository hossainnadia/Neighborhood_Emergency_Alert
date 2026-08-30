// CSRF Token সংগ্রহের ফাংশন
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Automatic Refresh Token হ্যান্ডলার
async function getValidToken() {
  let token = localStorage.getItem("access_token");
  const refresh = localStorage.getItem("refresh_token");

  if (!token && refresh) {
    try {
      const res = await fetch("/api/token/refresh/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: refresh }),
      });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem("access_token", data.access);
        token = data.access;
      } else {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
      }
    } catch (err) {
      console.error("Token refresh failed:", err);
    }
  }
  return token;
}

// Fetch API Wrapper (সকল Fetch রিকোয়েস্টে অথেন্টিকেশন যুক্ত করার জন্য)
async function apiFetch(url, options = {}) {
  const headers = options.headers || {};
  headers["Content-Type"] = "application/json";

  const csrfToken = getCookie("csrftoken");
  if (csrfToken) headers["X-CSRFToken"] = csrfToken;

  const token = await getValidToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  options.headers = headers;
  return fetch(url, options);
}
