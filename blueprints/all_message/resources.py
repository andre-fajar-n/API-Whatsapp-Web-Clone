from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_jwt_extended import get_jwt_claims
from blueprints import db, app, internal_required
from sqlalchemy import desc, or_
from datetime import datetime
import moment
import humanize

from blueprints.conversation.model import Conversations
from blueprints.list_group.model import ListGroup
from blueprints.member_group.model import MemberGroup
from blueprints.personal_messages.model import PersonalMessages
from blueprints.user.model import Users
from blueprints.group_message.model import MessageGroup

bp_all_message = Blueprint('union', __name__)
api = Api(bp_all_message)

class AllMessageResource(Resource):
    def options(self):
        return {'status': 'ok'}, 200

    @internal_required
    def get(self):
        claims = get_jwt_claims()

        list_chat = []

        # ambil data personal chat
        conversations = Conversations.query.filter(or_(Conversations.user1_id.like(claims['id']), Conversations.user2_id.like(claims['id'])))
        for conversation in conversations:
            marshal_conversation = marshal(
                conversation, Conversations.response_fields)

            # memasukkan data lawan chat
            if marshal_conversation['user1_id'] != claims['id']:
                user = Users.query.get(marshal_conversation['user1_id'])
                marshal_user = marshal(user, Users.response_fields)
                marshal_conversation['info_chat'] = marshal_user
            # memasukkan data lawan chat
            if marshal_conversation['user2_id'] != claims['id']:
                user = Users.query.get(marshal_conversation['user2_id'])
                marshal_user = marshal(user, Users.response_fields)
                marshal_conversation['info_chat'] = marshal_user

            # filter chat by user yang login
            personal_messages = PersonalMessages.query.filter_by(
                conversation_id=conversation.id)

            # mengambil data pesan terakhir
            last_personal_messages = personal_messages.order_by(desc(PersonalMessages.created_at)).first()
            marshal_last_personal_messages = marshal(last_personal_messages, PersonalMessages.response_fields)
            marshal_conversation['last_chat'] = marshal_last_personal_messages

            # mengambil semua chat
            list_message = []
            for personal_message in personal_messages:
                marshal_personal_message = marshal(
                    personal_message, PersonalMessages.response_fields)
                list_message.append(marshal_personal_message)

                # memasukkan data user yang mengirim chat selain user yang sedang login
                if marshal_personal_message['user_id'] == marshal_conversation['info_chat']['id']:
                    user = Users.query.get(
                        marshal_conversation['info_chat']['id'])
                    marshal_user = marshal(user, Users.response_fields)
                    marshal_personal_message['user'] = marshal_user

            marshal_conversation['all_chat'] = list_message

            list_chat.append(marshal_conversation)

        # ambil data group chat
        group_by_user = MemberGroup.query.filter_by(user_id=claims['id'])
        for group in group_by_user:
            # ambil group yang diikuti oleh user yang sedang login
            marshal_group = marshal(group, MemberGroup.response_fields)

            # memasukkan info group
            info_group = ListGroup.query.get(group.group_chat_id)
            marshal_info_group = marshal(info_group, ListGroup.response_fields)
            marshal_group['info_chat'] = marshal_info_group

            # filter chat by group
            chat_groups = MessageGroup.query.filter_by(
                group_chat_id=group.group_chat_id)

            # memasukkan data chat terakhir
            last_chat_group = chat_groups.order_by(
                desc(MessageGroup.created_at)).first()
            marshal_last_chat_group = marshal(
                last_chat_group, MessageGroup.response_fields)
            marshal_group['last_chat'] = marshal_last_chat_group

            # memasukkan semua chat
            all_chat_group = []
            for chat_group in chat_groups:
                marshal_chat_group = marshal(
                    chat_group, MessageGroup.response_fields)
                all_chat_group.append(marshal_chat_group)

                # memasukkan data user yang mengirim chat selain user yang sedang login
                if chat_group.user_id != claims['id']:
                    user = Users.query.get(chat_group.user_id)
                    marshal_user = marshal(user, Users.response_fields)
                    marshal_chat_group['user'] = marshal_user
            marshal_group['all_chat'] = all_chat_group

            list_chat.append(marshal_group)

            # mengurutkan berdasarkan chat terakhir
            for index1 in range(len(list_chat)-1):
                for index2 in range(0, len(list_chat) - index1 - 1):
                    earlier = list_chat[index2]['last_chat']['created_at']
                    more_late = list_chat[index2 + 1]['last_chat']['created_at']
                    if datetime.strptime(earlier, "%a, %d %b %Y %H:%M:%S %z") < datetime.strptime(more_late, "%a, %d %b %Y %H:%M:%S %z"):
                        c = list_chat[index2 + 1]
                        list_chat[index2 + 1] = list_chat[index2]
                        list_chat[index2] = c

        return list_chat, 200

api.add_resource(AllMessageResource, '')
