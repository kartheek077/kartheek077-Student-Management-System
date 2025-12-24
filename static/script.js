const API_URL = "http://127.0.0.1:5000";

// Register Student
function registerStudent() {
    fetch(`${API_URL}/register-student`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            student_name: document.getElementById("reg_name").value,
            mobile_number: document.getElementById("reg_mobile").value,
            email: document.getElementById("reg_email").value,
            branch: document.getElementById("reg_branch").value,
            is_passed_out: document.getElementById("reg_passed_out").checked
        })
    })
    .then(res => res.json())
    .then(data => alert(data.message));
}

// Retrieve Student
function getStudent() {
    const id = document.getElementById("get_id").value;
    fetch(`${API_URL}/retrieve-single-student?student_id=${id}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("student_result").innerText =
                JSON.stringify(data, null, 2);
        });
}

// Update Student
function updateStudent() {
    const id = document.getElementById("upd_id").value;

    fetch(`${API_URL}/update-student?student_id=${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            student_name: document.getElementById("upd_name").value,
            mobile_number: document.getElementById("upd_mobile").value,
            email: document.getElementById("upd_email").value,
            branch: document.getElementById("upd_branch").value,
            is_passed_out: document.getElementById("upd_passed_out").checked
        })
    })
    .then(res => res.json())
    .then(data => alert(data.message));
}

// Delete Student
function deleteStudent() {
    const id = document.getElementById("del_id").value;

    fetch(`${API_URL}/delete-student?student_id=${id}`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(data => alert(data.message));
}
