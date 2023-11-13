function setCookie(cname, cvalue, expire) {
  const d = new Date(expire);
  const expires = "expires=" + d.toUTCString();
  const cookie = cname + "=" + cvalue + ";" + expires + ";path=/;";
  document.cookie = cookie;
}


const form = document.forms[0]

form?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const t = e.target;
  const username = t.username.value;
  const password = t.password.value;
  await fetch("http://localhost:9000/api/auth/login",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: new URLSearchParams(
        {
          username: username,
          password: password
        })

    }).then((response) => response.json()).then((json) => {
      console.log(json)
      if (json?.token_type == "bearer") {
        setCookie("access_token", json?.access_token, json?.expire_access_token);
        setCookie("refresh_token", json?.refresh_token, json?.expire_refresh_token);
      }
    }).catch((err) => {
      console.err(err)
    });
});
