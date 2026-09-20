# Especificación Técnica de Arquitectura

## 1. Resumen Ejecutivo
La solución "TestSolution1" tiene como objetivo principal automatizar el envío recurrente de notificaciones por correo electrónico utilizando Microsoft Power Automate y Office 365 Outlook. Este flujo se ejecuta cada hora y envía un correo electrónico con una estampa de tiempo actualizada al destinatario especificado. La solución está diseñada para ser reutilizable y personalizable, lo que permite su integración con otros sistemas o flujos de trabajo en el entorno de Microsoft Dataverse.

El flujo utiliza una conexión predefinida a Office 365 Outlook para enviar correos electrónicos. No se detectaron tablas o entidades personalizadas en Dataverse asociadas con esta solución, lo que sugiere que su propósito es exclusivamente la automatización de procesos sin interacción directa con datos almacenados en Dataverse.

## 2. Inventario de Componentes

| Display Name             | Logical Name / Archivo                                      | Tipo              | Descripción / Propósito                                                                 |
|--------------------------|------------------------------------------------------------|-------------------|---------------------------------------------------------------------------------------|
| Notificación horario     | Notificacinhorario-2B44A048-0EB5-F111-AAAB-7C1E5287D75E.json | Flow              | Flujo recurrente que envía un correo electrónico con una estampa de tiempo cada hora. |
| Office 365 Outlook       | zsl_sharedoffice365_ee2b8                                   | Connection Reference | Conexión a Office 365 Outlook para enviar correos electrónicos.                       |
| TestSolution1            | Solution.xml                                               | Solution          | Contenedor de la solución que incluye el flujo y la conexión a Office 365 Outlook.   |

## 3. Modelo de Datos (Dataverse)
No aplica.

## 4. Lógica de Procesos (Power Automate)

### Descripción del Flujo: "Notificación horario"
Este flujo se ejecuta de manera recurrente cada hora, comenzando a partir del 20 de septiembre de 2026 a las 08:00 UTC. El flujo utiliza un trigger de tipo `Recurrence` y una acción principal para enviar un correo electrónico a un destinatario específico.

#### Detalles del Trigger
- **Tipo de Trigger:** Recurrence
- **Frecuencia:** Cada hora
- **Hora de inicio:** 2026-09-20T08:00:00Z

#### Detalles de la Acción
- **Nombre de la Acción:** Enviar correo electrónico (V2)
- **Tipo de Acción:** OpenApiConnection
- **Conexión:** Office 365 Outlook (zsl_sharedoffice365_ee2b8)
- **Parámetros del Correo:**
  - **Destinatario:** juan.hincapie@zerostatelabs.dev
  - **Asunto:** "Estampa de tiempo actual @{utcNow()}"
  - **Cuerpo:** "<p>Estampa de tiempo actual @{utcNow()}</p>"
  - **Importancia:** Normal

#### Diagrama de Flujo
```mermaid
flowchart TD
    A[Inicio: Trigger Recurrence] --> B[Enviar correo electrónico (V2)]
```

## 5. Interfaz de Usuario (Canvas / Model-Driven)
No aplica.