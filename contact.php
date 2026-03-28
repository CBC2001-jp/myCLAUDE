<?php
/**
 * contact.php — コンタクトフォーム送信処理
 * CBC Co., Ltd. お問い合わせフォームハンドラ
 */

// POST以外はトップへリダイレクト
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: index.php');
    exit;
}

// -------------------------------------------------------
// 設定
// -------------------------------------------------------
define('TO_EMAIL',   'info@cbc2001.com');
define('FROM_EMAIL', 'noreply@cbc2001.com');
define('SITE_NAME',  '有限会社シービーシー');

// -------------------------------------------------------
// 入力値の取得・サニタイズ
// -------------------------------------------------------
function sanitize(string $value): string {
    // 改行文字はスペースに変換してヘッダーインジェクション防止
    return trim(str_replace(["\r", "\n"], ' ', htmlspecialchars($value, ENT_QUOTES, 'UTF-8')));
}

$name         = sanitize($_POST['name']         ?? '');
$municipality = sanitize($_POST['municipality'] ?? '');
$email        = sanitize($_POST['email']        ?? '');
$message      = trim(htmlspecialchars($_POST['message'] ?? '', ENT_QUOTES, 'UTF-8'));

// -------------------------------------------------------
// バリデーション
// -------------------------------------------------------
$errors = [];

if ($name === '') {
    $errors[] = 'お名前は必須です。';
}
if ($municipality === '') {
    $errors[] = '自治体名・所属組織名は必須です。';
}
if ($email === '' || !filter_var($_POST['email'], FILTER_VALIDATE_EMAIL)) {
    $errors[] = '有効なメールアドレスを入力してください。';
}
if ($message === '') {
    $errors[] = 'ご相談内容は必須です。';
}

if (!empty($errors)) {
    header('Location: index.php?error=validation');
    exit;
}

// -------------------------------------------------------
// メール送信（管理者宛）
// -------------------------------------------------------
$subject = SITE_NAME . ' ウェブサイトよりお問い合わせ';

$body  = "以下の内容でお問い合わせがありました。\r\n";
$body .= "================================================\r\n";
$body .= "お名前　　　　：{$name}\r\n";
$body .= "自治体名・所属：{$municipality}\r\n";
$body .= "メールアドレス：{$email}\r\n";
$body .= "================================================\r\n";
$body .= "ご相談内容：\r\n{$message}\r\n";
$body .= "================================================\r\n";
$body .= "送信日時：" . date('Y-m-d H:i:s') . "\r\n";

$headers  = "From: " . FROM_EMAIL . "\r\n";
$headers .= "Reply-To: {$email}\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "MIME-Version: 1.0\r\n";

$adminSent = mail(TO_EMAIL, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers);

// -------------------------------------------------------
// 自動返信メール（送信者宛）
// -------------------------------------------------------
$autoSubject = SITE_NAME . ' お問い合わせを受け付けました';

$autoBody  = "{$name} 様\r\n\r\n";
$autoBody .= "このたびはお問い合わせいただきありがとうございます。\r\n";
$autoBody .= "以下の内容で受け付けました。内容を確認の上、担当者よりご連絡いたします。\r\n\r\n";
$autoBody .= "================================================\r\n";
$autoBody .= "お名前　　　　：{$name}\r\n";
$autoBody .= "自治体名・所属：{$municipality}\r\n";
$autoBody .= "メールアドレス：{$email}\r\n";
$autoBody .= "================================================\r\n";
$autoBody .= "ご相談内容：\r\n{$message}\r\n";
$autoBody .= "================================================\r\n\r\n";
$autoBody .= "─────────────────────────\r\n";
$autoBody .= SITE_NAME . "\r\n";
$autoBody .= "〒665-0803 兵庫県宝塚市花屋敷つつじガ丘1番20号\r\n";
$autoBody .= "Email: " . TO_EMAIL . "\r\n";
$autoBody .= "Tel: 080-3739-1963\r\n";
$autoBody .= "─────────────────────────\r\n";

$autoHeaders  = "From: " . SITE_NAME . " <" . FROM_EMAIL . ">\r\n";
$autoHeaders .= "Content-Type: text/plain; charset=UTF-8\r\n";
$autoHeaders .= "MIME-Version: 1.0\r\n";

mail($email, '=?UTF-8?B?' . base64_encode($autoSubject) . '?=', $autoBody, $autoHeaders);

// -------------------------------------------------------
// リダイレクト
// -------------------------------------------------------
if ($adminSent) {
    header('Location: index.php?sent=1');
} else {
    header('Location: index.php?error=mail');
}
exit;
