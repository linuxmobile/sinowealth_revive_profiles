# sinowealth_revive_profiles
🦄 This is a script, create by @_vaker_ . The script revive the profiles 2 and 3 from the SINOWEALTH USB Gaming Mouse

## Script para revivir el Mouse VSG Cyborg / Sinowealth.

El código obtiene los perfiles del mouse y reemplaza los perfiles 2 y 3 con una copia del perfil 1. Algunas cosas a destacar:

- El código utiliza la librería `hid` para comunicarse con el mouse a través de **HID (Human Interface Device, dispositivo de interfaz humana)**.
- La variable `needle` contiene el `vendor_id` y el `product_id` del mouse. Estos números se utilizan para filtrar los dispositivos `HID` **conectados** y **encontrar el mouse correcto**.
- La función `deviceFilter` se utiliza para filtrar la lista de dispositivos HID conectados y **devolver solo los que coinciden** con el `vendor_id` y el `product_id` del mouse.
- La función `findCommandDevice` busca el dispositivo que se puede utilizar para enviar comandos al mouse. Se hace esto enviando un reporte de característica específico (`cmd_feature_report`) y verificando si el envío fue exitoso. Si el envío fue exitoso, se devuelve el dispositivo; de lo contrario, se devuelve None.
- La función `findDataDevice` busca el dispositivo que se puede utilizar para obtener datos del mouse. Se hace esto solicitando un reporte de característica específico (especificado por el parámetro `report_id`) y verificando si la solicitud fue exitosa. Si la solicitud fue exitosa, se devuelve el dispositivo y el reporte de característica solicitado; **de lo contrario, se devuelve None**.
- La función `printProfile` imprime los datos del perfil proporcionados en un formato legible.
- La variable `profile_data` es una lista que se utilizará para almacenar los datos de cada perfil obtenidos del mouse.
- La línea devices = `list(enumerate(filter(deviceFilter, hid.enumerate())))` obtiene una lista de todos los dispositivos HID conectados y filtra la lista para que solo se incluyan los dispositivos que coinciden con el `vendor_id` y el `product_id` del mouse.
- Las siguientes líneas de código buscan y almacenan los dispositivos que se pueden utilizar para enviar comandos al mouse y obtener datos del mouse:

```python
dev_cmd = findCommandDevice(devices, cmd_feature_report)
dev_data, profile_data_temp = findDataDevice(devices, 4, 520)
profile_data.append(profile_data_temp)
```

- Si ambos dispositivos se han encontrado, el código solicita los datos de cada perfil al mouse y los almacena en la lista `profile_data`.

- Si el usuario da su consentimiento, **el código reemplaza los datos del perfil 2 y 3 con una copia de los datos del perfil 1**. Esto se hace enviando reportes de característica específicos al mouse para cambiar los perfiles y luego enviando un reporte de característica que contiene los datos del perfil 1 para sobrescribir los perfiles 2 y 3.


### Créditos:

- © [@_vaker_](https://gitlab.com/_vaker_/)