$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

const plusCartBtn = document.querySelectorAll('.plus-cart');
const minusCartBtn = document.querySelectorAll('.minus-cart');
const removeCartBtn = document.querySelectorAll('.remove-cart');
const amount = document.querySelector('#amount');
const totalAmount = document.querySelector('#total-amount');
const cartCaption = document.querySelector("#cart-caption");


// adding cart
for(let i=0; i<plusCartBtn.length; i++){
    plusCartBtn[i].addEventListener('click', function(){
        let prod_id = this.dataset.productid;

        let url = '/pluscart/';

        fetch(url, {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'productId':prod_id})
        }).then((response)=>{
            return response.json();
        }).then((data)=>{
            this.parentNode.children[2].textContent = data.quantity;
            amount.textContent = data.amount;
            totalAmount.textContent = data.total_amount;
        })
    })
}

// decreasing cart
for(let i=0; i<minusCartBtn.length; i++){
    minusCartBtn[i].addEventListener('click', function(){
        let prod_id = this.dataset.productid;

        let url = '/minuscart/';

        fetch(url, {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'productId':prod_id})
        }).then((response)=>{
            return response.json();
        }).then((data)=>{
            if (data.quantity != 0){
                this.parentNode.children[2].textContent = data.quantity;
            }
            else{
                const cart_body_div = this.parentNode.parentNode.parentNode.parentNode.parentNode;
                const html = `<div class="empty-cart-container d-flex align-items-center flex-column">
                <img src="{% static 'app/images/Empty_Cart.webp' %}" alt="" height="162px">
                <h5>Your cart is empty!</h5>
                <p>Explore our wide selection and find something you like</p>
              </div>`;
              cart_body_div.insertAdjacentHTML("afterbegin", html);
              cartCaption.style.display = 'none';
                this.parentNode.parentNode.parentNode.parentNode.remove();
            }
            amount.textContent = data.amount;
            totalAmount.textContent = data.total_amount;
        })
    })
}

//removing cart
for(let i=0; i<removeCartBtn.length; i++){
    removeCartBtn[i].addEventListener('click', function(){
        let prod_id = this.dataset.productid;

        let url = '/removecart/';

        fetch(url, {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'productId':prod_id})
        }).then((response)=>{
            return response.json();
        }).then((data)=>{
            amount.textContent = data.amount;
            totalAmount.textContent = data.total_amount;
            const cart_body_div = this.parentNode.parentNode.parentNode.parentNode.parentNode;
            const html = `<div class="empty-cart-container d-flex align-items-center flex-column">
            <img src="{% static 'app/images/Empty_Cart.webp' %}" alt="" height="162px">
            <h5>Your cart is empty!</h5>
            <p>Explore our wide selection and find something you like</p>
          </div>`;
          cart_body_div.insertAdjacentHTML("afterbegin", html);
          cartCaption.style.display = 'none';
            this.parentNode.parentNode.parentNode.parentNode.remove();
        })
    })
}