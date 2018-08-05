
$('.dnadd').click(function () {
    var table = $("tbody");
    table.append('<tr>\n' +
        '                                        <div class="cursor">\n' +
        '                                        <td>\n' +
        '                                            <input type="text" class="form-control path" value=""\n' +
        '                                           name="path"/>\n' +
        '                                        </td>\n' +
        '                                        <td>\n' +
        '                                            <select class="form-control option" name="option">\n' +
        '                                                <option value="md5">\n' +
        '                                                    MD5\n' +
        '                                                </option>\n' +
        '                                                <option value="regx">\n' +
        '                                                    REGX\n' +
        '                                                </option>\n' +
        '                                            </select>\n' +
        '                                        </td>\n' +
        '                                    <td>\n' +
        '                                        <input type="text" class="form-control content" value=""\n' +
        '                                           name="content"/>\n' +
        '                                        </td>\n' +
        '                                        <td>\n' +
        '                                        <input type="text" class="form-control hit" value=""\n' +
        '                                           name="hit"/>\n' +
        '                                        </td>\n' +
        '                                        <td>\n' +
        '                                        <button class="btn btn-block btn-md btn-custom waves-effect waves-light update" type="submit">Update</button>\n' +
        '                                            <button class="btn btn-block btn-md btn-custom waves-effect waves-light delete" type="submit">Delete</button>\n' +
        '                                        </td>\n' +
        '                                        <input type="hidden" class="_id" value="add" name="_id" />\n' +
        '                                            </div>\n' +
        '\n' +
        '                                    </tr>');

});

$(".table-edit").on("click","td .update",function () {
    var tr = $(this).parent().parent();

    var path = tr.find(".path").val();
    var option = tr.find(".option").val();
    var content = tr.find(".content").val();

    var hit = tr.find(".hit").val();
    var _id = tr.find("._id").val(); // add 添加指纹 update 更新指纹

    $.post(window.location.href,{
        "path":path,
        "option":option,
        "content":content,
        "hit":hit,
        "_id":_id
    },function (data,status) {
        console.log(data,status);
        if(data == "success"){
            swal("操作成功！","请继续操作","success");

        }else{

            swal("操作失败！","请重试","error");
        }

    })

});

$(".table-edit").on("click","td .delete",function () {
    var tr = $(this).parent().parent();
    var content = tr.find("._id").val();
    $.post(window.location.href,{
        "delete":content
    },function (data,status) {
        console.log(data,status);
        if(data == "success"){
            swal("操作成功！","请继续操作","success");
        }else{
            swal("操作失败！","请重试","error");
        }

    });
    tr.remove();
});