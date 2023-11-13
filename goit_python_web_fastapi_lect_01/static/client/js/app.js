const token = localStorage.getItem("access_token");
const BASE_URL = "http://localhost:9000";

console.log(`token=${token}`);

get_cats = async () => {
  const URL = `${BASE_URL}/api/cats`;
  const response = await fetch(URL, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (response.ok) {
    cats.innerHTML="";
    result = await response.json();
    for (cat of result) {
      el = document.createElement("li");
      el.className = "list-group-item";
      el.innerHTML = `ID: ${cat?.id} Name: <strong>${cat?.nickname}</strong> Status: ${cat?.vaccinated} Owner: ${cat?.owner.email}`;
      cats.appendChild(el);
    }
  }
};

get_owners = async () => {
  const URL = `${BASE_URL}/api/owners`;
  const response = await fetch(URL, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (response.ok) {
    owners.innerHTML="";
    result = await response.json();
    for (owner of result) {
      el = document.createElement("li");
      el.className = "list-group-item";
      el.innerHTML = `ID: ${owner?.id} Email: <strong>${owner?.email}</strong>`;
      owners.appendChild(el);
    }
  }
};

get_cats();
get_owners();
