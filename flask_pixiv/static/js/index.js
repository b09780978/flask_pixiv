function add_button(id, url) {
  swal({
        title: "你確定要加入嗎?",
        text: "你將要加入這張圖片",
        type: "info",
        showCancelButton: true,
        confirmButtonClass: "btn-info",
        confirmButtonText: "Yes, add it!",
        closeOnConfirm: false,
        showLoaderOnConfirm: true
        },
        function () {
              $.ajax({
                  url: '/api/pixiv/',
                  method: 'POST',
                  dataType: 'json',
                  contentType: 'application/json; charset=UTF-8',
                  data: JSON.stringify({ 'id' : id, 'url' : url}),
                }).success(function (data, textStatus, jqXHR) {
                    location.reload();
                }).error(function (jqXHR, textStatus, errorThrown) {
                    console.log(jqXHR);
                    location.reload();
                });
            });
}