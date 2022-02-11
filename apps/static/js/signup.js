function phtycFunction(checked = true) {
  var checkb = document.getElementById('phtyc')
  checkb.checked = checked
  var myModalEl = document.getElementById('phtycModal')
  var modal = bootstrap.Modal.getInstance(myModalEl) 
  modal.hide()   
}

function phtdpFunction(checked = true) {
  var checkb = document.getElementById('phtdp')
  checkb.checked = checked
  var myModalEl = document.getElementById('phtdpModal')
  var modal = bootstrap.Modal.getInstance(myModalEl) 
  modal.hide()
}