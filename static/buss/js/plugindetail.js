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
            $.post('/task_del', {oid: oid}, function (e) {
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