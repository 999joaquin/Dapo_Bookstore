document.getElementById('orderForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const bookId = document.getElementById('book_id').value;
    const quantity = document.getElementById('quantity').value;
    
    fetch('http://127.0.0.1:5003/order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            book_id: bookId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 200) {
            document.getElementById('orderResult').innerHTML = `
                <h3>Order Details:</h3>
                <p>Book: ${data.order_details.book.title}</p>
                <p>Author: ${data.order_details.author.name}</p>
                <p>Quantity: ${data.order_details.quantity}</p>
                <p>Total Price: $${data.order_details.total_price}</p>
            `;
        } else {
            document.getElementById('orderResult').innerHTML = `<p>${data.message}</p>`;
        }
    })
    .catch(error => {
        document.getElementById('orderResult').innerHTML = `<p>Error: ${error.message}</p>`;
    });
});

document.getElementById('bookForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const bookId = document.getElementById('new_book_id').value;
    const title = document.getElementById('title').value;
    const authorId = document.getElementById('author_id').value;
    
    fetch('http://127.0.0.1:5001/create_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: bookId,
            title: title,
            author_id: authorId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            document.getElementById('bookResult').innerHTML = `
                <h3>Book Created Successfully:</h3>
                <p>ID: ${data.data.id}</p>
                <p>Title: ${data.data.title}</p>
                <p>Author ID: ${data.data.author_id}</p>
            `;
        } else {
            document.getElementById('bookResult').innerHTML = `<p>${data.message}</p>`;
        }
    })
    .catch(error => {
        document.getElementById('bookResult').innerHTML = `<p>Error: ${error.message}</p>`;
    });
});
