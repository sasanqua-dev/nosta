// csrf_tokenの取得に使う
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}
function settings_ajax_handler(type) {
    var csrf_token = getCookie('csrftoken');
    path = "/";
    if (type == 'save') {
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrf_token);
                }
            },
            type: 'POST',
            url: path,
            data: {
                type: 'post_change_user_data',
                email: document.getElementById('email').value,
                first_name: document.getElementById('first_name').value,
                last_name: document.getElementById('last_name').value,
            },
            dataType: 'text',
        })
            .done(function (data) {
                window.alert('更新しました\n表示されている情報が更新されるまで時間がかかる場合があります');
            })
            .fail(function (data) {
                // error
                console.log(data);
                window.alert('通信エラーが発生しました(E-UA100)');
            });
    } else if ((type = 'password')) {
        if (document.getElementById('password').value != document.getElementById('password2').value) {
            window.alert('パスワードが一致しません');
            return;
        }
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrf_token);
                }
            },
            type: 'POST',
            url: path,
            data: {
                type: 'post_password_user_data',
                old_password: document.getElementById('old_password').value,
                password: document.getElementById('password').value,
            },
            dataType: 'text',
        })
            .done(function (data) {
                if ((data = 'error')) {
                    window.alert('現在のパスワードが間違っています');
                    return;
                }
                window.alert('更新しました');
            })
            .fail(function (data) {
                // error
                console.log(data);
                window.alert('通信エラーが発生しました(E-UA100)');
            });
    } else if ((type = 'delete')) {
        let checkSaveFlg = window.confirm('アカウントを削除すると紐づいているすべての情報が削除されます\n本当によろしいですか？');
        if (checkSaveFlg) {
            $.ajax({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader('X-CSRFToken', csrf_token);
                    }
                },
                type: 'POST',
                url: path,
                data: {
                    type: 'post_delete_user_data',
                },
                dataType: 'text',
            })
                .done(function (data) {
                    if (data == 'error') {
                        window.alert('予約中の注文または予約中、発券中のチケットがあるためアカウントを削除できません');
                    }
                })
                .fail(function (data) {
                    // error
                    console.log(data);
                    window.alert('通信エラーが発生しました(E-UA100)');
                });
        } else {
        }
    } else if (type='cancel'){
        let checkSaveFlg = window.confirm('この注文をキャンセルします\n本当によろしいですか？');
        if (checkSaveFlg) {
            $.ajax({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader('X-CSRFToken', csrf_token);
                    }
                },
                type: 'POST',
                url: path,
                data: {
                    type: 'cancel',
                    id: document.getElementById("pid").value
                },
                dataType: 'text',
            })
                .done(function (data) {
                    if (data == 'error') {
                        window.alert('キャンセル不可の商品が含まれています');
                    }
                })
                .fail(function (data) {
                    // error
                    console.log(data);
                    window.alert('通信エラーが発生しました(E-UA100)');
                });
        } else {
        }
    }
}
function getdetail(id){
    var csrf_token = getCookie('csrftoken');
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        },
        type: 'POST',
        url: "/",
        data: {
            type: 'get_detail',
            id: id
        },
        dataType: 'html',
    })
        .done(function (data) {
            document.getElementById("odetail").innerHTML = data
            openModal(document.getElementById("detail_modal"))
        })
        .fail(function (data) {
            // error
            console.log(data);
            window.alert('通信エラーが発生しました(E-UA100)');
        });
}
