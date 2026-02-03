## Доповнення крутить FastAPI сервер, до якого HomeAssistant звертається по URL: http://localhost:8010 (порт налаштовується)
## Список підтримуваних ендпоінтів:

### 1) Ендпоінт **/rf_toe** - Графік погодинних відключень (ГПВ) від Тернопіль-обленерго з офіційного сайту [https://toe.com.ua](https://www.toe.com.ua/)
приклад видає ГПВ, по заданих параметрах: http://localhost:8010/rf_toe?group=1.2&cityId=1111&streetId=11111&buildingNames=1а
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
```

### 2) Ендпоінт **.fetch** - Парсинг динамічних веб сторінок
приклад http://localhost:8010/fetch?url=url.for.load&selector=.class1

