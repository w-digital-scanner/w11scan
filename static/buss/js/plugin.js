$('.dropify').dropify({
    messages: {
        'default': 'Drag and drop a file here or click',
        'replace': 'Drag and drop or click to replace',
        'remove': 'Remove',
        'error': 'Ooops, something wrong appended.'
    },
    error: {
        'fileSize': 'The file size is too big (1M max).'
    }
});

$('.uploadjson').css('display', '');

$('#field-type').change(function () {
    if ($(this).val() == 'json') {
        $('.uploadjson').css('display', '');
        $('.uploadfile').css('display', 'none');
    } else if ($(this).val() == 'script') {
        $('.uploadjson').css('display', 'none');
        $('.uploadfile').css('display', '');
    } else {
        $('.uploadjson').css('display', 'none');
        $('.uploadfile').css('display', 'none');
    }
});

$(".portlet #edit").each(
    function (i) {
        $(this).click(function () {
            var cmsname = $(this).attr("data-cms");
            console.log(cmsname);
            $("#con-change-modal").modal('hide');
        })
    }
);

$("#search_bar").bind('keypress',function (event) {
    if(event.keyCode == "13"){
       keyword = $(this).val();
       if(keyword == ""){
           window.location.href = '/plugin';
       }else{
           window.location.href = '/plugin/' + keyword;
       }


    }
});

$('.zmdi-close').click(function () {
    var oid = $(this).attr('id');
    swal({
            title: "确认删除？",
            text: "所有删除操作将不可逆，请谨慎操作",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            closeOnConfirm: false
        },
        function () {
            $.post('/deleteplugin', {oid: oid}, function (e) {
                if (e == 'success') {
                    swal("已删除", '', "success");
                    $('#' + oid).parent().parent().parent().parent().remove()
                }
                else {
                    swal("删除失败", '', "error");
                }
            })

        });
});