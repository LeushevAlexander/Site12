$(document).on("click", ".NomenModal", function () {    
     var myNomenId = $(this).data('id');
     //$(".modal-body #NomenId").val( myNomenId );
     //var id;     
     //$('[data-target="#StaticModal"]').click(function(){ id = this.id; });

     $(".modal-body #NomenId").val( 'My Id' );

     // As pointed out in comments,
     // it is unnecessary to have to manually call the modal.
     // $('#addBookDialog').modal('show');
});    
