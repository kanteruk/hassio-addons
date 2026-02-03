Доповнення крутить FastAPI сервер, до якого HomeAssistant звертається по УРЛу http://localhost:8010, порт налаштовується

Сервер сприймає такий ендпоінт http://localhost:8010/rf_toe?group=1.2&cityId=1111&streetId=11111&buildingNames=1а
і видає графік погодинних відключень від Тернопіль-обленерго, по заданих параметрах.
Приклад як використовую, додаю в configuration.yaml:
```
rest:
  - resource: http://localhost:8010/rf_toe?group=1.2&cityId=1111&streetId=11111&buildingNames=1а
    scan_interval: 300
    sensor:
      - unique_id: toe_gpv_1_2
        name: toe_gpv_1_2
        value_template: >
          {% set v = value_json.ranges %}
          {{ v if v not in [None, '', 'unknown'] else this.state }}        
        availability: >
          {{ value_json is not none
             and value_json.date_create is defined
             and value_json.date_create not in ['', 'unknown'] }}          
        json_attributes:
        - group
        - date_create
        - date_graph
        - times_off
        - times_count
        - ranges
