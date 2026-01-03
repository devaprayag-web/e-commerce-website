$(document).ready(function () {
    $('.paywithrazorpay').on('click', function (e) {
        e.preventDefault();

        var firstname = $("[name='firstname']").val();
        var lastname = $("[name='lastname']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if (
            firstname === "" || lastname === "" || email === "" ||
            phone === "" || address === "" || city === "" ||
            state === "" || country === "" || pincode === ""
        ) {
            swal("Alert!", "All fields are mandatory!", "error");
            return;
        }

        $.ajax({
            method: "GET",
            url: "/proceed-to-pay/",
            success: function (response) {

                var options = {
                    "key": "rzp_test_bvs9fcMzpUjePo",
                    "amount": response.total_price * 100,
                    "currency": "INR",
                    "name": "Amritha_Madampully",
                    "description": "Thank you for buying from us",
                    "handler": function (razorpay_response) {

                        $.ajax({
                            method: "POST",
                            url: "/placeorder/",
                            data: {
                                firstname: firstname,
                                lastname: lastname,
                                email: email,
                                phone: phone,
                                address: address,
                                city: city,
                                state: state,
                                country: country,
                                pincode: pincode,
                                payment_mode: "paid by razorpay",
                                payment_id: razorpay_response.razorpay_payment_id,
                                csrfmiddlewaretoken: token
                            },
                            success: function (responsec) {
                                swal("Success!", responsec.status, "success")
                                    .then(() => {
                                        window.location.href = "/order/";
;
                                    });
                            }
                        });
                    },
                    "prefill": {
                        "name": firstname + " " + lastname,
                        "email": email,
                        "contact": phone
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                };

                var rzp1 = new Razorpay(options);
                rzp1.open();
            },
            error: function (xhr) {
                console.log(xhr.responseText);
                swal("Error!", "Could not proceed to payment.", "error");
            }
        });
    });
});
