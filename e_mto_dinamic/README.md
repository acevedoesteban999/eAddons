# eProductDinamic  
This module lets you create products that use a dinamic Bill of Materials. The goal is to sell dinamic or customized products based on a static list of components, while still being able to vary quantities and the final price.

### Dinamic Product Assignment  
- Configure the product as “Dinamic” and assign a Dinamic Bill of Materials.
    ![IMAGE](static/description/assets/screenshots/1.png)  
### Sale  
- When a dinamic product is added to the sale, a pop-up opens where the user can choose quantities from the dinamic BOM and set the final price.  
    ![IMAGE](static/description/assets/screenshots/2.png)
- Upon confirming the sale, no default picking is created for this product; instead, it is replaced by a manufacturing order.  
    ![IMAGE](static/description/assets/screenshots/3.png)