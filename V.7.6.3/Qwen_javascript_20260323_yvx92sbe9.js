// 🔧 ЗАМЕНИТЕ на ID вашего шаблона Google Docs
const TEMPLATE_ID = 'ВАШ_DOCUMENT_ID_ЗДЕСЬ';
const FOLDER_ID = 'ВАШ_FOLDER_ID_ЗДЕСЬ'; // Папка для сохранённых PDF

function onEdit(e) {
  const sheet = e.source.getActiveSheet();
  const range = e.range;
  
  // Проверяем, что редактирован столбец F (Статус)
  if (sheet.getName() !== 'Certificates' || range.getColumn() !== 6) {
    return;
  }
  
  const row = range.getRow();
  const status = e.value;
  
  // Если статус = "Отправить", генерируем сертификат
  if (status === 'Отправить') {
    generateCertificate(row);
  }
}

function generateCertificate(row) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Certificates');
  const data = sheet.getRange(row, 1, 1, 7).getValues()[0];
  
  const [date, firstName, lastName, email, course, status, sentDate] = data;
  
  // Проверяем, не отправлен ли уже
  if (sentDate) {
    Logger.log('Уже отправлен');
    return;
  }
  
  // Генерируем PDF
  const pdfId = createPDF(firstName, lastName, course, date);
  const pdfUrl = `https://drive.google.com/file/d/${pdfId}/view`;
  
  // Отправляем email
  sendEmail(email, firstName, lastName, course, pdfUrl);
  
  // Обновляем статус
  sheet.getRange(row, 6).setValue('Отправлен');
  sheet.getRange(row, 7).setValue(new Date());
}

function createPDF(firstName, lastName, course, date) {
  const template = DriveApp.getFileById(TEMPLATE_ID);
  const folder = DriveApp.getFolderById(FOLDER_ID);
  
  // Копируем шаблон
  const copy = template.makeCopy(`Сертификат_${firstName}_${lastName}`, folder);
  const doc = DocumentApp.openById(copy.getId());
  const body = doc.getBody();
  
  // Заменяем переменные
  body.replaceText('{{FirstName}}', firstName);
  body.replaceText('{{LastName}}', lastName);
  body.replaceText('{{Course}}', course);
  body.replaceText('{{Date}}', Utilities.formatDate(new Date(), 'UTC', 'dd.MM.yyyy'));
  
  doc.saveAndClose();
  
  // Конвертируем в PDF
  const pdf = DriveApp.getFileById(copy.getId()).getAs('application/pdf');
  const pdfFile = folder.createFile(pdf);
  pdfFile.setName(`Сертификат_${firstName}_${lastName}.pdf`);
  
  // Удаляем временный Google Doc
  copy.setTrashed(true);
  
  return pdfFile.getId();
}

function sendEmail(email, firstName, lastName, course, pdfUrl) {
  const subject = `Ваш сертификат от RAGIMOFF - ${course}`;
  
  const body = `
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
      <p>Здравствуйте, <strong>${firstName} ${lastName}</strong>!</p>
      
      <p>Поздравляем вас с успешным завершением курса:</p>
      <p style="font-size: 18px; color: #c8a96e;"><strong>"${course}"</strong></p>
      
      <p>Ваш сертификат во вложении.</p>
      
      <p style="margin-top: 30px;">
        С уважением,<br>
        <strong>Кəнан Rəhimov</strong><br>
        Həkim Psixoterapevt<br>
        <a href="https://ragimoff.org">ragimoff.org</a>
      </p>
    </body>
    </html>
  `;
  
  GmailApp.sendEmail(email, subject, body, {
    htmlBody: body,
    name: 'RAGIMOFF - Кəнан Rəhimov'
  });
}