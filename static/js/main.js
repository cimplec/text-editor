$(document).ready(function() {
    document.getElementById('simc_code').addEventListener('keydown', function(e) {
        if (e.key == 'Tab') {
            e.preventDefault();
            var start = this.selectionStart;
            var end = this.selectionEnd;
    
            this.value = this.value.substring(0, start) + "\t" + this.value.substring(end);
    
            this.selectionStart = this.selectionEnd = start + 1;
        }
    });

    $("#compile_code").click(function() {
        var simc_code = $("#simc_code").val();

        if(simc_code != "") {
            $.ajax({
                url: "/compile",
                type: "post",
                data: {"simc_code": simc_code},
                success: function(result) {
                    $("#c_code").val("");
                    if(result.status == "error") {
                        alert(result.message);
                    } else if(result.status == "success") {
                        $("#c_code").val(result.message);
                    }
                }
            });
        } else {
            alert("Cannot compile empty code!");
        }
    });
});