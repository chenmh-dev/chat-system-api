# Chat System API Design v1

## 1. API Overview
    POST /conversations/direct
    GET /conversations
    GET /conversations/<conversation_id>
    GET /conversations/<conversation_id>/messages
    POST /conversations/<conversation_id>/messages

## 2. Auth Rules
    用户可以创建多个会话
    一个会话可以包含多个用户
    一个会话下可以有多条消息

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
    Success - 201 Conversation created
    Success - 200 Conversation found

### 3.1.10 Error Cases
    400 BadRequest: target_user_id must be integer
    401 Unauthorization
    403 无权限
    404 NotFound: user not found

### 3.1.11 Service Responsibility
    判断目标是否存在
    判断会话是否存在

### 3.2.1 Endpoint
    GET /conversations

### 3.2.2 Purpose
    查看当前用户有哪些会话

### 3.2.3 Auth
    需要登录

### 3.2.4 Path Params
    None

### 3.2.5 Query Params
    user_id: int, 当前登录用户的id
    
### 3.2.6 Request Body
    {}

### 3.2.7 Validation Rules
    None

### 3.2.8 Business Rules
    查看当前user_id下有哪些convasation_id

### 3.2.9 Response
    Success - 200 Conversations found

### 3.2.10 Error Cases
    None

### 3.2.11 Service Responsibility
    找到当前user_id所拥有的conversation_id

### 3.3.1 Endpoint
    GET /conversations/<conversation_id>/introduction

### 3.3.2 Purpose
    查看当前用户的某个会话的详情

### 3.3.3 Auth
    需要登录

### 3.3.4 Path Params
    conversation_id，int, conversation表的id

### 3.3.5 Query Params
    user_id: int, 当前登录用户的id
    conversation_id，int, conversation表的id

### 3.3.6 Request Body
    {}

### 3.3.7 Validation Rules
    None

### 3.3.8 Business Rules
    查看当前user_id下的convasation_id的详情

### 3.3.9 Response
    Success - 200 Conversations introduction

### 3.3.10 Error Cases
    404 NotFound: convasation not found

### 3.3.11 Service Responsibility
    查看当前user_id下的convasation_id的详情

## 4. Message APIs

### 4.1.1 Endpoint
    GET /conversations/<conversation_id>

### 4.1.2 Purpose
    查看某个会话下的消息

### 4.1.3 Auth
    需要登录
    需要在会话内

### 4.1.4 Path Params
    conversation_id：int， 表conversation的id

### 4.1.5 Query Params
    conversation_id：int， 表conversation的id
    user_id: int, 当前登录用户的id

### 4.1.6 Request Body
    {}

### 4.1.7 Validation Rules
    None

### 4.1.8 Business Rules
    conversation_id存在
    user_id和conversation_id在同一个conversation中

### 4.1.9 Response
    Success - 200 Messages

### 4.1.10 Error Cases
    404 NotFound: conversation not found

### 4.1.11 Service Responsibility
    判断会话是否存在
    判断当前用户是否在查询的会话中

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
    conversation_id：int， 表conversation的id
    user_id: int, 当前登录用户的id
    content:str, 发送的消息
    
### 4.2.6 Request Body
    {
        "content": ""
    }

### 4.2.7 Validation Rules
    必须是字符串，not None，可以是空字符串

### 4.2.8 Business Rules
    conversation_id存在
    user_id和conversation_id在同一个conversation中

### 4.2.9 Response
    Success - 200 Message created

### 4.2.10 Error Cases
    404 NotFound: conversation not found

### 4.2.11 Service Responsibility
    判断会话是否存在
    判断当前用户是否在查询的会话中





    