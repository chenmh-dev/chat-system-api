# Chat System API Design v2

## 1. API Overview
    POST /conversations/direct
    GET /conversations
    GET /conversations/<conversation_id>
    GET /conversations/<conversation_id>/messages
    POST /conversations/<conversation_id>/messages

## 2. Auth Rules
    All endpoints require authentication.

    User identity is derived from token.

    Conversation resources can only be accessed by members.

## 3. Conversation APIs

### 3.1.1 Endpoint
    POST /conversations/direct

### 3.1.2 Purpose
    和目标用户之间建立会话

### 3.1.3 Auth
    需要登录

### 3.1.4 Path Params
    None

### 3.1.5 Query Params
    None

### 3.1.6 Request Body
    {
        "target_user_id": 2
    }

### 3.1.7 Validation Rules
    target_user_id: 必填，int

### 3.1.8 Business Rules
    目标必须存在
    不能与自己创建会话
    寻找与目标的会话
    没有则创建与目标的会话
    创建两条member_ship

### 3.1.9 Response 
    Success - 201 OK
    {
    "success": true,
    "message": "Conversation created",
    "data": []
    }

    Success - 200 OK
    {
    "success": true,
    "message": "Conversation found",
    "data": []
    }
### 3.1.10 Error Cases
    400 BadRequest: target_user_id must be integer
    401 Unauthorized: Ivalid token or expired
    403 Forbidden: can not conversation with yourself
    404 NotFound: user not found

### 3.1.11 Service Responsibility
    寻找会话时确认目标存在
    寻找会话时确认与目标的会话存在
    创建会话时确认会话目标不是自己

### 3.2.1 Endpoint
    GET /conversations

### 3.2.2 Purpose
    查看当前用户有哪些会话

### 3.2.3 Auth
    需要登录

### 3.2.4 Path Params
    None

### 3.2.5 Query Params
    page: int, 可空，默认值：1， 页数
    page_size: int, 可空，默认值：10，一页的大小
    sort: str, 可空，默认值：id，排序的字段
    order: str， 可空，默认值：desc，选择是递增还是递减
    keyword: str 可空，默认值：None，查询的关键字
    
### 3.2.6 Request Body
    {}

### 3.2.7 Validation Rules
    None

### 3.2.8 Business Rules
    获取当前用户id
    查看当前用户的所有会话

### 3.2.9 Response
    Success - 200 OK
    {
    "success": true,
    "message": "Conversations found",
    "data": []
    }
### 3.2.10 Error Cases
    400 BadRequest: Bad request
    401 Unauthorized: Ivalid token or expired
    403 Forbidden: Forbidden
    404 NotFound: Convasation Not found

### 3.2.11 Service Responsibility
    查看当前用户的所有会话

### 3.3.1 Endpoint
    GET /conversations/<conversation_id>

### 3.3.2 Purpose
    查看当前用户的某个会话的详情

### 3.3.3 Auth
    需要登录

### 3.3.4 Path Params
    conversation_id，int, conversation表的id

### 3.3.5 Query Params
    None

### 3.3.6 Request Body
    {}

### 3.3.7 Validation Rules
    None

### 3.3.8 Business Rules
    获取当前用户id
    在member_ship表中筛选具有当前用户id的数据
 
### 3.3.9 Response
    Success - 200 OK
    {
    "success": true,
    "message": "Conversation",
    "data": []
    }

### 3.3.10 Error Cases
    400 BadRequest: Bad request
    401 Unauthorized: Ivalid token or expired
    403 Forbidden: Forbidden
    404 NotFound: Convasation Not found

### 3.3.11 Service Responsibility
    在member_ship表中筛选具有当前用户id的数据

## 4. Message APIs

### 4.1.1 Endpoint
    GET /conversations/<conversation_id>/messages

### 4.1.2 Purpose
    查看某个会话下的消息

### 4.1.3 Auth
    需要登录
    需要在会话内

### 4.1.4 Path Params
    conversation_id：int， 表conversation的id

### 4.1.5 Query Params
    None

### 4.1.6 Request Body
    {}

### 4.1.7 Validation Rules
    None

### 4.1.8 Business Rules
    获取当前用户id
    确认conversation_id属于当前用户
    查询conversation_id下的所有消息

### 4.1.9 Response
    Success - 200 OK
    {
    "success": true,
    "message": "Messages",
    "data": []
    }

### 4.1.10 Error Cases
    400 BadRequest: Bad request
    401 Unauthorized: Ivalid token or expired
    403 Forbidden: Forbidden

### 4.1.11 Service Responsibility
    确认conversation_id属于当前用户
    查询conversation_id下的所有消息

### 4.2.1 Endpoint
    POST /conversations/<conversation_id>/messages

### 4.2.2 Purpose
    在某个会话中发送消息

### 4.2.3 Auth
    需要登录
    需要在会话内

### 4.2.4 Path Params
    conversation_id：int， 表conversation的id

### 4.2.5 Query Params
    None
    
### 4.2.6 Request Body
    {
        "content": "language"
    }

### 4.2.7 Validation Rules
    必须是字符串，not None，可以是空字符串

### 4.2.8 Business Rules
    验证用户输入合法
    获取当前用户id
    确认conversation_id属于当前用户
    创建一条message

### 4.2.9 Response
    Success - 201 OK
    {
    "success": true,
    "message": "Message created",
    "data": []
    }

### 4.2.10 Error Cases
    400 BadRequest: Bad request
    401 Unauthorized: Ivalid token or expired
    403 Forbidden: Forbidden
    404 NotFound: Conversation Not found

### 4.2.11 Service Responsibility
    确认conversation_id属于当前用户
    创建一条message





    