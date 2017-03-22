
$(function() {

  //----------------------- state & skills & exp ------------------------------

    var state_number = $(".ensign_state_number");
    var exp = $("#ensign_exp");
    var skill_check = $(".ensign_skill_checkbox");
    
      state_number.attr("max", function(){
        if (parseInt(exp.val())>=10){
          return parseInt($(this).val())+1;
        } else {
          return parseInt($(this).val());
        }
      });

      state_number.attr("min", function(){return parseInt($(this).val())});

      state_number.on("change",function(){
        if (parseInt(this.value)>parseInt(this.defaultValue)) {
          exp.val(parseInt(exp.val())-10);
        } else{
          exp.val(parseInt(exp.val())+10);
        }
        exp.trigger("change");
      });

      skill_check.on("click", function(event){
          var is_check =  $(this).attr("checked") == "checked" ? 0 : 1;
          if (is_check) {
            if (parseInt(exp.val()) < 10) {
              alert("Experience not enough!");
              event.preventDefault();
              event.stopPropagation();
              return;
            };
            exp.val(parseInt(exp.val())-10);
            $(this).attr('checked', true);
          } else {
            exp.val(parseInt(exp.val())+10);
            $(this).attr('checked', false);
          }
          exp.trigger("change");
      });

      exp.on("change", function(){
        if (parseInt(this.value)<10) {
          state_number.attr("max", function(){
            return parseInt($(this).val());
          });
        } else{
          state_number.attr("max", function(){
            return parseInt(this.defaultValue)+1;
          });
        }
      });

      // ----------------------- item modal -------------------------------

      var ensign_item_limit = 4;
      var ensign_weapon_limit = 1;

      var ensign_item_btn = $("#ensign_item_btn");
      var ensign_item_modal = $("#ensign_item_modal");
      var old_ensign_item_cost = $("#old_ensign_item_cost");

      ensign_item_btn.click(function(){
          var checked_items = $('.ensign_item:checked');
          var cost = 0;
          for (var i = 0; i < checked_items.length; i++) {
            cost += parseInt($(checked_items[i]).siblings().text());
          };

          old_ensign_item_cost.val(cost);
          ensign_item_modal.modal('show');
      });


      $("#ensign_item_ok").click(function(){
        var checked_items = $('.ensign_item:checked');
        var checked_weapons = $('.ensign_weapon:checked');
        var checked_other_items = $('.ensign_other_item:checked');


        if (checked_items.length > ensign_item_limit){
          alert("ensigns can only carry 6 items.");
          return;
        }
        if (checked_weapons.length > ensign_weapon_limit){
          alert("ensigns can only carry 2 weapons.");
          return;
        }

        var cost = 0;
        for (var i = 0; i < checked_items.length; i++) {
          cost += parseInt($(checked_items[i]).siblings().text());
        };
        var real_cost = cost-parseInt(old_ensign_item_cost.val());
        if(!update_currency(real_cost)){return;}

        var weapons = "";
        var items = "";

        for (var i = 0; i < checked_weapons.length; i++) {
          weapons += (checked_weapons[i].value+",");
        };

        weapons = weapons.replace(/,\s*$/, "");

        for (var i = 0; i < checked_other_items.length; i++) {
          items += (checked_other_items[i].value+",");
        };
        items = items.replace(/,\s*$/, "");

        $("#ensign_weapon_p").text(weapons);
        $("#ensign_item_p").text(items);
        
        old_ensign_item_cost.val(cost);
        ensign_item_modal.modal("hide");

      });

      function update_currency(cost){
        var rest_currency = parseInt(currency.val()) - cost;
        if (rest_currency < 0) {
          alert("currency not enough!");
          return false;
        };

        currency.val(rest_currency);
        return true;
      }

});
