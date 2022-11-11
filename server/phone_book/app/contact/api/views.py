from aiohttp.web_response import json_response

from aiohttp_apispec import docs, request_schema, response_schema, json_schema

from phone_book.app.contact.models import Contact
from phone_book.app.contact.schemas import ContactListSchema, NewContactSchema, ExistedContactSchema
from phone_book.app.web.app import View


class ContactListView(View):
    @response_schema(ContactListSchema)
    async def get(self):
        contacts = await self.request.app.contact_accessor.get_contact_list()
        return json_response(
            status=200,
            data={
                "contacts": [ExistedContactSchema().dump(contact) for contact in contacts]
            }
        )

    @request_schema(NewContactSchema)
    @response_schema(ExistedContactSchema)
    async def post(self):
        data = await self.request.json()
        contact = Contact(**data)
        new_contact = await self.request.app.contact_accessor.create_contact(contact)
        response = ExistedContactSchema().dump(new_contact)
        return json_response(
            status=200,
            data={
                "contact": response
            }
        )

    @response_schema(ContactListSchema)
    async def delete(self):
        contacts = await self.request.app.contact_accessor.get_contact_list()
        await self.request.app.contact_accessor.delete_all_contacts()
        return json_response(
            status=200,
            data={
                "contacts": [ExistedContactSchema().dump(contact) for contact in contacts]
            }
        )


class ContactView(View):
    @response_schema(ExistedContactSchema)
    async def get(self):
        uid = self.request.match_info["uid"]
        contact = await self.request.app.contact_accessor.get_contact_by_uid(uid)
        return json_response(status=200, data=ExistedContactSchema().dump(contact))

    @request_schema(ExistedContactSchema)
    @response_schema(ExistedContactSchema)
    async def put(self):
        data = await self.request.json()
        contact = Contact(**data)
        edited_contact = await self.request.app.contact_accessor.edit_contact(contact)
        return json_response(
            status=200,
            data=ExistedContactSchema().dump(edited_contact)
        )

    @response_schema(ExistedContactSchema)
    async def delete(self):
        uid = self.request.match_info["uid"]
        contact = await self.request.app.contact_accessor.delete_contact_by_uid(uid)
        return json_response(
            status=200,
            data=ExistedContactSchema().dump(contact)
        )
