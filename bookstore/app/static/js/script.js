function updateCartUI(data){

    let counters = document.getElementsByClassName("cart-counter");
        for (let c of counters)
            c.innerText = data.total_quantity;

        let amount = document.getElementsByClassName("cart-amount");
        for (let c of amount)
            c.innerText = data.total_amount.toLocaleString();
}

function addToCart(id, name, price) {
    fetch('/api/carts', {
        method: "POST",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {

        let counters = document.getElementsByClassName("cart-counter");
        for (let c of counters)
            c.innerText = data.total_quantity;
    })
}

function updatecart(bookId, obj){
    fetch(`/api/carts/${bookId}`,{
        method:"put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {

        updateCartUI(data)
    })
}

function deletecart(bookId){
    if (confirm("Bạn có chắn chắn muốn xóa không?")===true){
        fetch(`/api/carts/${bookId}`,{
        method:"delete"
    }).then(res => res.json()).then(data => {

        updateCartUI(data);

        document.getElementById(`cart${bookId}`).style.display = "none"
    })
    }
}

function pay(){
    if (confirm("Bạn có muốn thanh toán không?")===true){
        fetch("/api/pay",{
            method:"post"
        }).then(res => res.json()).then(data => {
            if(data.status === 200) {
                alert("Thanh toán thành công!");
                location.reload();
            }
        })
    }
}
