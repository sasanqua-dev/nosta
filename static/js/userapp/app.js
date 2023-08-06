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
    path = '/app/';
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
                username: document.getElementById('username').value,
                nickname: document.getElementById('nickname').value,
            },
            dataType: 'text',
        })
            .done(function (data) {
                if (data == 'e_error') {
                    window.alert('このメールアドレスはすでに使用されています');
                    return;
                } else if (data == 'u_error') {
                    window.alert('このユーザー名はすでに使用されています');
                    return;
                } else if (data == 'ure_error') {
                    window.alert('ユーザー名は半角英数字のみが使用できます');
                    return;
                }
                window.alert('更新しました\n表示されている情報が更新されるまで時間がかかる場合があります');
                location.reload();
            })
            .fail(function (data) {
                // error
                console.log(data);
                window.alert('通信エラーが発生しました(E-UA100)');
            });
    } else if (type == 'delete') {
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
                    location.reload();
                })
                .fail(function (data) {
                    // error
                    console.log(data);
                    window.alert('通信エラーが発生しました(E-UA100)');
                });
        } else {
        }
    } else if (type == 'cancel') {
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
                    id: document.getElementById('pid').value,
                },
                dataType: 'text',
            })
                .done(function (data) {
                    if (data == 'error') {
                        window.alert('キャンセル不可の商品が含まれています');
                        return;
                    }
                    window.alert('注文をキャンセルしました');
                    location.reload();
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
function getdetail(id) {
    var csrf_token = getCookie('csrftoken');
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        },
        type: 'POST',
        url: '/app/',
        data: {
            type: 'get_detail',
            id: id,
        },
        dataType: 'html',
    })
        .done(function (data) {
            document.getElementById('odetail').innerHTML = data;
            makeorderQR();
            openModal(document.getElementById('order_detail'));
        })
        .fail(function (data) {
            // error
            console.log(data);
            window.alert('通信エラーが発生しました(E-UA100)');
        });
}
function makeorderQR() {
    var id = document.getElementById('pid').value;
    var secret = document.getElementById('secret').value;
    var qrtext = 'order:' + id + '/' + secret;
    var utf8qrtext = unescape(encodeURIComponent(qrtext));
    $('#img-qr-ordercode').html('');
    $('#img-qr-ordercode').qrcode({ width: 200, height: 200, text: utf8qrtext });
}

function favorites(type, id, via) {
    var csrf_token = getCookie('csrftoken');
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        },
        type: 'POST',
        url: '/app/',
        data: {
            type: 'post_fav',
            action: type,
            id: id,
        },
        dataType: 'html',
    })
        .done(function (data) {
            if (via === 'market') {
                let number = document.getElementById('favorite').firstElementChild.textContent;
                if (type === 'fav') {
                    document.getElementById('favorite').setAttribute('hidden', '');
                    document.getElementById('unfavorite').removeAttribute('hidden');
                    document.getElementById('favorite').firstElementChild.lastElementChild.textContent = Number(number) + 1;
                    document.getElementById('unfavorite').firstElementChild.lastElementChild.textContent = Number(number) + 1;
                } else if (type === 'unfav') {
                    document.getElementById('favorite').removeAttribute('hidden');
                    document.getElementById('unfavorite').setAttribute('hidden', '');
                    document.getElementById('favorite').firstElementChild.lastElementChild.textContent = Number(number) - 1;
                    document.getElementById('unfavorite').firstElementChild.lastElementChild.textContent = Number(number) - 1;
                }
            } else if (via === 'app') {
                document.getElementById(id).remove();
            }
        })
        .fail(function (data) {
            // error
            console.log(data);
        });
}
