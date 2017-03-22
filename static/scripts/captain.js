
$(function() {

    

	//----------------------- state and exp -------------------------------

	  var state_number = $(".captain_state_number");
	  var exp = $(".captain_exp");
	  
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

      var captain_item_limit = 6;
      var captain_weapon_limit = 2;

      var captain_item_btn = $("#captain_item_btn");
      var captain_item_modal = $("#captain_item_modal");
      var old_captain_item_cost = $("#old_captain_item_cost");

      captain_item_btn.click(function(){
          var checked_items = $('.captain_item:checked');
          var cost = 0;
          for (var i = 0; i < checked_items.length; i++) {
            cost += parseInt($(checked_items[i]).siblings().text());
          };

          old_captain_item_cost.val(cost);
          captain_item_modal.modal('show');
      });


      $("#captain_item_ok").click(function(){
        var checked_items = $('.captain_item:checked');
        var checked_weapons = $('.captain_weapon:checked');
        var checked_other_items = $('.captain_other_item:checked');


        if (checked_items.length > captain_item_limit){
          alert("Captains can only carry 6 items.");
          return;
        }
        if (checked_weapons.length > captain_weapon_limit){
          alert("Captains can only carry 2 weapons.");
          return;
        }

        var cost = 0;
        for (var i = 0; i < checked_items.length; i++) {
          cost += parseInt($(checked_items[i]).siblings().text());
        };
        var real_cost = cost-parseInt(old_captain_item_cost.val());
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

        $("#captain_weapon_p").text(weapons);
        $("#captain_item_p").text(items);

        old_captain_item_cost.val(cost);
        captain_item_modal.modal("hide");

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
