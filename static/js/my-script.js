function clearForm() {
    // 获取表单元素
    var form = document.getElementById("myForm");
    // 对输入字段进行遍历
    for (var i = 0; i < form.elements.length; i++) {
        var element = form.elements[i];
        // 如果该元素是输入字段，则将其值设置为空字符串
        if (element.type !== "submit") {
            element.value = "";
        }
    }
}

function checkForm(form) {
    // 获取表单中的所有输入框
    var inputs = form.getElementsByTagName('input');

    // 遍历所有输入框
    for (var i = 0; i < inputs.length; i++) {
        // 检查输入框是否为空
        if (inputs[i].value === '') {
            alert('请填写所有信息');
            return false;
        }
    }

    // 表单验证通过
    return true;
}