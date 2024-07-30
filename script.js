document.getElementById('addPersonForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const firstname = document.getElementById('firstname').value;
    const lastname = document.getElementById('lastname').value;
    const email = document.getElementById('email').value;
    const telephone = document.getElementById('telephone').value;

    const response = await fetch('/api/add_person', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ firstname, lastname, email, telephone }),
    });

    const data = await response.json();
    if (data.success) {
        const qr = new QRCode(document.getElementById("qrcode"), data.qr_data);
    } else {
        alert('Error adding person');
    }
});

let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
scanner.addListener('scan', async function (content) {
    const response = await fetch('/api/verify_access', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: content }),
    });

    const data = await response.json();
    document.getElementById('result').innerText = data.message;
});

Instascan.Camera.getCameras().then(function (cameras) {
    if (cameras.length > 0) {
        scanner.start(cameras[0]);
    } else {
        console.error('No cameras found.');
    }
}).catch(function (e) {
    console.error(e);
});
