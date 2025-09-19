// Fetch and display tasks
async function loadTasks() {
  const res = await fetch("/tasks", {
    headers: {
      "Authorization": "Bearer " + localStorage.getItem("token")
    }
  });
  const tasks = await res.json();
  const list = document.getElementById("task-list");
  list.innerHTML = "";
  tasks.forEach(task => {
    const item = document.createElement("li");
    item.textContent = `${task.task_name}: ${task.task_description}`;
    const delBtn = document.createElement("button");
    delBtn.textContent = "Delete";
    delBtn.onclick = () => deleteTask(task.id);
    item.appendChild(delBtn);
    list.appendChild(item);
  });
}

// Add a new task
async function addTask() {
  const task_name = document.getElementById("task-name").value;
  const task_description = document.getElementById("task-desc").value;

  await fetch("/tasks", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + localStorage.getItem("token")
    },
    body: JSON.stringify({ task_name, task_description })
  });

  document.getElementById("task-name").value = "";
  document.getElementById("task-desc").value = "";

  loadTasks(); // Refresh task list
}

// Delete a task
async function deleteTask(id) {
  await fetch(`/tasks/${id}`, {
    method: "DELETE",
    headers: {
      "Authorization": "Bearer " + localStorage.getItem("token")
    }
  });

  loadTasks(); // Refresh task list
}

// Logout
function logout() {
  localStorage.removeItem("token");
  window.location.href = "/";
}

// Load tasks on page load
window.onload = loadTasks;

// LOGIN.HTML
async function login() {
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const res = await fetch("/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData
  });

  const data = await res.json();
if (res.status === 200 && data.access_token) {
  localStorage.setItem("token", data.access_token);
  window.location.href = "/dashboard";
} else {
  alert(data.detail || "Login failed");
}
}

function goToSignup() {
  window.location.href = "/signup";
}

// SIGNUP.HTML
function handleSignup(event) {
  event.preventDefault(); // prevent page reload

  const name = document.getElementById("signup-username").value;
  const password = document.getElementById("signup-password").value;

  // Optional: collect other fields (not used in backend yet)
  const fullName = document.getElementById("full-name").value;
  const phone = document.getElementById("phone").value;
  const gender = document.getElementById("gender").value;

  fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, password })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.message || "Signup successful");
    if (data.message) {
      window.location.href = "/"; // redirect to login
    }
  })
  .catch(err => {
    console.error("Signup error:", err);
    alert("Signup failed");
  });
}