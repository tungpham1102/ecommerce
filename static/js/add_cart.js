// update-cart có ở chỗ Add to Cart button và + - 1 số lượng
// gán class name update-cart cho biên updateCart của js
updateCart = document.getElementsByClassName('update-cart')

// lặp tất cả các button with class name : update-cart, vì là có 2 action add, và remove,
// nên cần lặp và kiểm tra xem nó là action gì

// gán, lấy id, action tại mỗi update-cart button
for(var i = 0; i < updateCart.length; i++) {
    // click button Add To Cart in store.html with class name 'add-to-cart'
    // đặt biến updateCart là 1 Listener, sử dụng action click trên html.
    // khi click thì sẽ có 1 function xử lý biến updateCart
    updateCart[i].addEventListener('click', function(){
        // lấy giá trị của id và action
        // at button add-to-cart in store.html, productId = data-product = '{{ product.id }}', string
        var productId = this.dataset.product
        // at button add-to-cart in store.html, action = data-action = 'add', string
        var action = this.dataset.action

        console.log('productId: ', productId, 'action: ', action);

        // show at console user: tungpham1029, if user not yet logged, it show AnonymousUser
        console.log('User: ',user)
        // xét nếu đã đăng nhập hay chưa đăng nhập
        if ( user == "AnonymousUser"){
            // nếu chưa đăng nhập thì nó sẽ xử lý bằng function này
            addCookieItem(productId, action)
        } else {
            // còn nếu đăng nhập rồi thì nó sẽ xử lý function này
            console.log('update user is running')
            // do updateUserOrder if you logged in
            updateUserOrder(productId, action)
        }
    })
}

// function xử lý button add to cart khi chưa đăng nhập.
// tức là nó vẫn sẽ tạo ra 1 customer nhưng nó không tạo ra user
function addCookieItem(productId, action){
    console.log('User is not authenticated')

    if (action == 'add'){
        if (cart[productId] == undefined){
            // nếu chưa có sản phẩm này trong order_item thì nó sẽ được tạo và sẽ tạo 1 sản phầm
            cart[productId] = {'quantity':1}
        } else {
            // còn nếu đã có thì nó sẽ cộng thêm 1
            cart[productId]['quantity'] += 1
        }
    }
    if (action == 'remove'){
        // nếu là action remove, nó sẽ có tại trang cart.html, thì số lượng quantity của sản phẩm được click sẽ trừ đi 1
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <= 0){
        // nếu sản phẩm có số lượng nhỏ hơn 0 thì sẽ xoá luôn sản phẩm này trong order_item
            console.log('remove Item')
            delete cart[productId]
        }
    }
    if (action == 'trash'){
        delete cart[productId]
    }
    console.log("Cart: ",cart)
    document.cookie = 'cartCookie= '+JSON.stringify(cart) + ";domain=;path=/"
    // reload lại trang lúc này
    location.reload()
}

// nếu đã loggin user thì function này sẽ xử lý
// update order với các biến là id của sản phẩm với action add or remove
function updateUserOrder(productId, action){
    console.log('User is logged in, sending data...')
    // handle from update_item at views
    var url = '/update_item/'
    // cấu trúc cần có khi fetch js từ python
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        // data productId, action from data-product, data-action at button Add To Cart
        body: JSON.stringify({'productId' : productId, 'action': action})
    })
    // promise
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data: ',data)
        // load lại page khi click button add-to-cart
        location.reload()
    })
}
