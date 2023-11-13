function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  console.log(document.cookie)
}


const form = document.forms[0]

form?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const t = e.target;
  const username = t.username.value;
  const password = t.password.value;
  const response = await fetch("http://localhost:9000/api/auth/login",
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
