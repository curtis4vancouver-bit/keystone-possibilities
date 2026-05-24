import { NextRequest, NextResponse } from "next/server";
import { google } from "googleapis";
// @ts-ignore
import MailComposer from "nodemailer/lib/mail-composer";

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB per-file
const MAX_TOTAL_SIZE = 20 * 1024 * 1024; // 20MB total batch

export async function POST(req: NextRequest) {
  try {
    const contentTypeHeader = req.headers.get("content-type") || "";
    if (!contentTypeHeader.includes("multipart/form-data")) {
      return NextResponse.json(
        { error: "Invalid Content-Type header. Expected multipart/form-data." },
        { status: 415 }
      );
    }

    const formData = await req.formData();
    
    const clientName = formData.get("name")?.toString().trim() || "";
    const clientEmail = formData.get("email")?.toString().trim() || "";
    const organization = formData.get("company")?.toString().trim() || "Unspecified Org";
    const serviceTopic = formData.get("topic")?.toString().trim() || "General Consult";
    const bodyText = formData.get("message")?.toString().trim() || "";

    if (!clientName || !clientEmail || !bodyText) {
      return NextResponse.json(
        { error: "Missing required inputs: name, email, or message." },
        { status: 400 }
      );
    }

    const fileEntries = formData.getAll("attachments");
    const parsedAttachments: any[] = [];
    let processedTotalSize = 0;

    for (const entry of fileEntries) {
      if (entry instanceof File && entry.name !== "" && entry.size > 0) {
        if (entry.size > MAX_FILE_SIZE) {
          return NextResponse.json(
            { error: `Attachment error: '${entry.name}' exceeds the 10MB limit.` },
            { status: 400 }
          );
        }

        processedTotalSize += entry.size;
        if (processedTotalSize > MAX_TOTAL_SIZE) {
          return NextResponse.json(
            { error: "Attachment limit exceeded: Total batch size must not exceed 20MB." },
            { status: 400 }
          );
        }

        const rawBuffer = Buffer.from(await entry.arrayBuffer());
        parsedAttachments.push({
          filename: entry.name,
          content: rawBuffer,
          contentType: entry.type || "application/octet-stream",
        });
      }
    }

    const htmlEmailContent = constructSparkHtmlBody({
      clientName,
      clientEmail,
      organization,
      serviceTopic,
      bodyText,
    });

    const oauth2Client = new google.auth.OAuth2(
      process.env.GOOGLE_CLIENT_ID,
      process.env.GOOGLE_CLIENT_SECRET
    );

    oauth2Client.setCredentials({
      refresh_token: process.env.GOOGLE_REFRESH_TOKEN,
    });

    const mailOptions = {
      from: `"${clientName}" <${process.env.KEYSTONE_GMAIL_USER}>`,
      replyTo: `"${clientName}" <${clientEmail}>`,
      to: process.env.KEYSTONE_GMAIL_USER,
      subject: `[Keystone Portal Entry] ${serviceTopic} - ${organization}`,
      text: `Portal Submission:\nName: ${clientName}\nEmail: ${clientEmail}\nOrg: ${organization}\nMessage: ${bodyText}`,
      html: htmlEmailContent,
      attachments: parsedAttachments,
    };

    const mailCompiler = new MailComposer(mailOptions);
    const rawCompiledMessage: Buffer = await new Promise((resolve, reject) => {
      mailCompiler.compile().build((err: any, msg: any) => {
        if (err) return reject(err);
        resolve(msg);
      });
    });

    const webSafeBase64String = rawCompiledMessage
      .toString("base64")
      .replace(/\+/g, "-")
      .replace(/\//g, "_")
      .replace(/=+$/, "");

    const gmailInstance = google.gmail({ version: "v1", auth: oauth2Client });

    const apiReceipt = await gmailInstance.users.messages.send({
      userId: "me",
      requestBody: {
        raw: webSafeBase64String,
      },
    });

    return NextResponse.json({
      status: "success",
      message: "Email successfully delivered via Gmail REST API",
      id: apiReceipt.data.id,
    }, { status: 200 });

  } catch (error: any) {
    console.error("Critical error in Gmail API Route handler:", error);
    return NextResponse.json(
      { error: "Failed to dispatch REST API transaction.", details: error.message },
      { status: 500 }
    );
  }
}

function constructSparkHtmlBody(data: {
  clientName: string;
  clientEmail: string;
  organization: string;
  serviceTopic: string;
  bodyText: string;
}): string {
  const sanitize = (val: string) =>
    val.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

  const sName = sanitize(data.clientName);
  const sEmail = sanitize(data.clientEmail);
  const sOrg = sanitize(data.organization);
  const sTopic = sanitize(data.serviceTopic);
  const sText = sanitize(data.bodyText).replace(/\n/g, "<br />");

  return `
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="color-scheme" content="light dark" />
  <meta name="supported-color-schemes" content="light dark" />
  <title>Portal Submission</title>
  <style type="text/css">
    body, table, td, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
    table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
    table { border-collapse: collapse!important; }
    body { height: 100%!important; margin: 0!important; padding: 0!important; width: 100%!important; background-color: #f7f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    
    @media (prefers-color-scheme: dark) {
     .bg-outer { background-color: #121212!important; }
     .bg-inner { background-color: #1c1c1e!important; }
     .text-title { color: #ffffff!important; }
     .text-desc { color: #a1a1a6!important; }
     .table-row { background-color: #2c2c2e!important; border-bottom: 1px solid #3a3a3c!important; }
    }
  </style>
</head>
<body class="bg-outer" style="margin: 0; padding: 0; background-color: #f7f9fa;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%" class="bg-outer" style="background-color: #f7f9fa;">
    <tr>
      <td align="center" style="padding: 40px 10px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="bg-inner" style="max-width: 600px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); overflow: hidden;">
          <tr>
            <td align="center" style="padding: 30px; background-color: #101010;">
              <h1 style="margin: 0; color: #ffffff; font-size: 20px; font-weight: 700; letter-spacing: -0.3px;">Keystone Portal Submission</h1>
            </td>
          </tr>
          <tr>
            <td style="padding: 30px 30px 10px 30px;">
              <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr class="table-row" style="background-color: #fafbfc; border-bottom: 1px solid #ededed;">
                  <td style="padding: 12px 16px; width: 35%; font-size: 11px; font-weight: 700; color: #7f7f84; text-transform: uppercase;" class="text-desc">Client Name</td>
                  <td style="padding: 12px 16px; font-size: 14px; color: #111111; font-weight: 500;" class="text-title">${sName}</td>
                </tr>
                <tr class="table-row" style="background-color: #ffffff; border-bottom: 1px solid #ededed;">
                  <td style="padding: 12px 16px; font-size: 11px; font-weight: 700; color: #7f7f84; text-transform: uppercase;" class="text-desc">Email Address</td>
                  <td style="padding: 12px 16px; font-size: 14px; color: #0070f3; font-weight: 500;"><a href="mailto:${sEmail}" style="color: #0070f3; text-decoration: none;">${sEmail}</a></td>
                </tr>
                <tr class="table-row" style="background-color: #fafbfc; border-bottom: 1px solid #ededed;">
                  <td style="padding: 12px 16px; font-size: 11px; font-weight: 700; color: #7f7f84; text-transform: uppercase;" class="text-desc">Company</td>
                  <td style="padding: 12px 16px; font-size: 14px; color: #111111; font-weight: 500;" class="text-title">${sOrg}</td>
                </tr>
                <tr class="table-row" style="background-color: #ffffff; border-bottom: 1px solid #ededed;">
                  <td style="padding: 12px 16px; font-size: 11px; font-weight: 700; color: #7f7f84; text-transform: uppercase;" class="text-desc">Topic</td>
                  <td style="padding: 12px 16px; font-size: 14px; color: #111111; font-weight: 500;" class="text-title">${sTopic}</td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="padding: 20px 30px 40px 30px;">
              <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td style="padding-bottom: 10px; border-bottom: 2px solid #111111; font-size: 12px; font-weight: bold; color: #111111;" class="text-title">SUBMITTED INQUIRY</td>
                </tr>
                <tr>
                  <td style="padding-top: 15px; font-size: 15px; line-height: 1.62; color: #2d2d2d;" class="text-title">
                    ${sText}
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding: 24px 30px; background-color: #fafbfc; border-top: 1px solid #eaeaea;">
              <p style="margin: 0; font-size: 10px; color: #a1a1a6; text-transform: uppercase; letter-spacing: 0.5px;" class="text-desc">Keystone Inc. Automated Processing Unit</p>
            </td>
          </tr>
        </table>
        </td>
    </tr>
  </table>
</body>
</html>
  `.trim();
}
