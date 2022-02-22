(function() {
    console.log('Virtual DOM');
})();

function handleClick(type) {
    fetch('/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: type
            }),
        })
        .then(response => response.json())
        .then(data => {
            getStatus(data.task_id)
        })
}

function getStatus(taskID) {
    fetch(`/tasks/${taskID}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(res => {
            //console.log(res)
            var status_css = "text-warning";
            if (res.task_status == "SUCCESS") {
                status_css = "text-success";
            } else if (res.task_status == "FAILURE") {
                status_css = "text-danger";
            } else if (res.task_status == "RETRY") {
                status_css = "text-info";
            }
            const html = `
            <tr id="${res.task_id}">
                <td>${taskID}</td>
                <td class="${status_css}">${res.task_status}</td>
                <td>${res.ready}</td>
            </tr>`;
            console.log(document.getElementById(taskID))
            if(!!document.getElementById(taskID)) {
                // document.getElementById(taskID).replaceWith(html);
                document.getElementById(taskID).remove()
            }
            document.getElementById('tasks').innerHTML = html + document.getElementById('tasks').innerHTML;
            // const newRow = document.getElementById('tasks').insertRow(0);
            //       newRow.innerHTML = html;
            
            const taskStatus = res.task_status;
            if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return false;
            setTimeout(function() {
                getStatus(res.task_id);
            }, 1000);
        })
        .catch(err => console.log(err));
}