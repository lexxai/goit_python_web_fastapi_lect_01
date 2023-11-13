const token = localStorage.getItem("access_token");
const BASE_URL = "http://localhost:9000";

console.log(`token=${token}`);

function setLoading(target) {
    target.innerHTML='<div class="alert alert-primary" role="alert">Loading...</div>'
}

get_cats = async () => {
  const URL = `${BASE_URL}/api/cats`;
  const response = await fetch(URL, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (response.ok) {
    cats.innerHTML = "";
    result = await response.json();
    for (cat of result) {
      el = document.createElement("li");
      el.className = "list-group-item";
      el.innerHTML = `ID: ${cat?.id} Name: <strong>${cat?.nickname}</strong> Status: ${cat?.vaccinated} Owner: ${cat?.owner.email}`;
      cats.appendChild(el);
    }
  }else if  (response.status == 401) {
    window.location = "index.html"
  }
};

get_owners = async () => {
  setLoading(owners);
  const URL = `${BASE_URL}/api/owners`;
  const response = await fetch(URL, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (response.ok) {
    owners.innerHTML = "";
    result = await response.json();
    for (owner of result) {
      el = document.createElement("li");
      el.className = "list-group-item";
      el.innerHTML = `ID: ${owner?.id} Email: <strong>${owner?.email}</strong>`;
      owners.appendChild(el);
    }
  }else if  (response.status == 401) {
    window.location = "index.html"
  }
};

ownerCreate.addEventListener("submit", async (e) => {
  e.preventDefault();
  const URL = `${BASE_URL}/api/owners/`;
  const raw = JSON.stringify({
    email: ownerCreate?.email?.value,
  });
  const response = await fetch(URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: raw,
  });
  if (response.status == 201) {
    ownerCreate.reset();
    get_owners();
  }else if  (response.status == 401) {
    window.location = "index.html"
  }
});

get_cats();
get_owners();
