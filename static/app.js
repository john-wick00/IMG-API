document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData();
    formData.append('image', document.getElementById('image').files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.image_url) {
            var list = document.getElementById('imageList');
            var listItem = document.createElement('li');
            listItem.innerHTML = `Image URL: <a href="${data.image_url}" target="_blank">${data.image_url}</a>`;
            list.appendChild(listItem);
        }
    })
    .catch(err => console.log(err));
});
