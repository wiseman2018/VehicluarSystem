$('.datepicker').datepicker({
    orientation: 'bottom',
    icons: {
        time: 'fa fa-clock-o',
        date: 'fa fa-calendar',
        up: 'fa fa-chevron-up',
        down: 'fa fa-chevron-down',
        previous: 'fa fa-chevron-left',
        next: 'fa fa-chevron-right',
        today: 'fa fa-crosshairs',
        clear: 'fa fa-trash'
    }
});



$("#btn_filter").click(function () {
    var start_date = $("#start_date").val();
    var end_date = $("#end_date").val();

    getReport(start_date, end_date);

});

$('a.confirm_delete').click(function (e) {
    e.preventDefault();
    var url = this.href;
    var msg_ = $(this).data('msg');
    var title_ = $(this).data('title');

    swal({
        title: typeof title_ !== 'undefined' ? title_ : 'Are you sure?',
        text: typeof msg_ !== 'undefined' ? msg_ : "Are you sure you want to delete the selected item?",
        icon: 'warning',
        buttons: {
            cancel: {
                text: 'No, cancel',
                value: null,
                visible: true,
                className: "",
                closeModal: false
            },
            confirm: {
                text: 'Yes, go ahead!',
                value: true,
                visible: true,
                className: "bg-danger",
                closeModal: false
            }
        }
    }).then(function (isConfirm) {
        if (isConfirm) {
            self.location = url;
        } else {
            swal('Cancelled', 'Operation has been cancelled.', 'error');
        }
    });

});


